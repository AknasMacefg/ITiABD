import csv
import json
import ssl
import math
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.csv"
SEEDS_FILE = BASE_DIR / "seeds_url.csv"

COLUMNS = [
    "наименование у поставщика",
    "производитель",
    "наличие на складе, шт.",
    "цена за штуку при требуемом количестве (с учётом ценовых порогов)",
    "минимальная партия",
    "кратность упаковки",
    "валюта",
    "включён ли НДС",
    "срок поставки",
    "стоимость доставки в Москву",
    "минимальная сумма заказа",
    "ссылка на страницу",
    "дата и время получения данных",
]

REQUIRED = {
    "ATmega328P-AU": 1,
    "кварцевый резонатор 16 МГц HC-49S": 1,
    "LM358DR": 1,
    "конденсатор керамический 0805 22 пФ C0G 50 В": 2,
    "резистор 0805 1 кОм ±5%": 8,
    "стабилизатор AMS1117-3.3": 1,
    "конденсатор керамический 0805 100 нФ X7R 50 В": 10,
}

SITES = [
    "chipdip.ru",
    "promelec.ru",
    "platan.ru",
    "dip8.ru",
    "ampero.ru",
]

CRAWL_DELAY = {
    "chipdip.ru": 2.0,
    "promelec.ru": 2.0,
    "platan.ru": 10.0,
    "dip8.ru": 2.0,
    "ampero.ru": 2.0,
}

_last_request = {}
_robots_cache = {}
_user_agent = "EducationalCatalogCollector/1.0 (contact: not supplied)"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.scripts = []
        self._in_script = False
        self._script_type = ""
        self._script_data = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key:
                self.meta[key.lower()] = attrs.get("content", "")
        elif tag == "script":
            self._in_script = True
            self._script_type = attrs.get("type", "").lower()
            self._script_data = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_script:
            self.scripts.append((self._script_type, "".join(self._script_data)))
            self._in_script = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_script:
            self._script_data.append(data)
        if data.strip():
            self.text.append(data.strip())


def host_allowed(url):
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    if not any(host == site or host.endswith("." + site) for site in SITES):
        return False, "Ссылка ведёт не на один из разрешённых сайтов"

    robots_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/robots.txt", "", ""))
    if robots_url in _robots_cache:
        return _robots_cache[robots_url]

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": _user_agent})
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=20, context=context) as response:
            robots_text = response.read().decode("utf-8", errors="replace")
        rp.parse(robots_text.splitlines())
    except Exception as exc:
        result = False, f"Не удалось прочитать robots.txt: {exc}"
        _robots_cache[robots_url] = result
        return result
    if not rp.can_fetch(_user_agent, url):
        result = False, "robots.txt запрещает эту страницу"
        _robots_cache[robots_url] = result
        return result
    result = True, ""
    _robots_cache[robots_url] = result
    return result


def polite_get(url, timeout=10):
    allowed, reason = host_allowed(url)
    if not allowed:
        raise PermissionError(reason)

    host = urllib.parse.urlparse(url).hostname or ""
    matched = next((s for s in SITES if host == s or host.endswith("." + s)), host)
    delay = CRAWL_DELAY.get(matched, 2.0)
    elapsed = time.time() - _last_request.get(matched, 0)
    if elapsed < delay:
        time.sleep(delay - elapsed)

    req = urllib.request.Request(url, headers={
        "User-Agent": _user_agent,
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ssl._create_unverified_context()) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
    _last_request[matched] = time.time()
    return body


def parse_jsonld_objects(data):
    for script_type, script in data.scripts:
        if "ld+json" not in script_type:
            continue
        try:
            obj = json.loads(script)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, list):
            yield from obj
        else:
            yield obj


def first(obj, *keys):
    if not isinstance(obj, dict):
        return None
    for key in keys:
        if key in obj:
            return obj[key]
    return None


def parse_number(text):
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    import re
    match = re.search(r"[0-9][0-9\s\u00a0]*(?:[.,][0-9]+)?", str(text))
    if not match:
        return None
    value = match.group(0).replace(" ", "").replace("\u00a0", "")
    if "," in value:
        value = value.replace(".", "").replace(",", ".")
    elif value.count(".") == 1 and len(value.rsplit(".", 1)[1]) == 2:
        pass
    else:
        value = value.replace(".", "")
    return float(value)


def parse_page(url):
    import re
    html = polite_get(url)
    parser = TextExtractor()
    parser.feed(html)
    host = urllib.parse.urlparse(url).hostname or ""

    name = parser.meta.get("og:title") or parser.title
    manufacturer = ""
    price = None
    currency = "н/д"
    stock = None
    moq = 1
    packing = 1
    vat = "н/д"
    thresholds = []

    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if h1:
        name = re.sub(r"<[^>]+>", "", h1.group(1)).strip()

    for obj in parse_jsonld_objects(parser):
        if not isinstance(obj, dict) or obj.get("@type") != "Product":
            continue
        name = first(obj, "name") or name
        manufacturer = first(obj, "manufacturer") or manufacturer
        brand = first(obj, "brand")
        if not manufacturer and isinstance(brand, dict):
            manufacturer = first(brand, "name") or ""
        offers = first(obj, "offers")
        if isinstance(offers, list):
            offers = offers[0] if offers else None
        if isinstance(offers, dict):
            price = parse_number(first(offers, "price", "lowPrice", "highPrice")) or price
            currency = first(offers, "priceCurrency") or currency
            availability = str(first(offers, "availability") or "")
            if "InStock" in availability:
                stock = "в наличии"

    if host in ("www.chipdip.ru", "chipdip.ru"):
        gtag_brand = re.search(r'"brand":"([^"]+)"', html)
        keywords = re.search(r'<meta name="keywords" content="([^"]+)"', html, re.I)
        if gtag_brand:
            manufacturer = gtag_brand.group(1)
        elif keywords:
            parts = [p.strip() for p in keywords.group(1).split(",")]
            manufacturer = parts[-1] if len(parts) >= 3 else ""
        discount_match = re.search(r'data-discounts="([^"]+)"', html)
        if discount_match:
            raw = discount_match.group(1)
            thresholds = [(float(q), float(p)) for q, p in re.findall(r"\[([0-9]+),([0-9.]+)", raw)]
        price = thresholds[0][1] if thresholds else None
        if price is not None:
            currency = "RUB"
        if 'itemprop="availability" href="https://schema.org/InStock"' in html:
            stock = "в наличии"
        vat = "да"

    elif host in ("www.promelec.ru", "promelec.ru"):
        price_matches = re.findall(r'data-index-price="([0-9]+)">(.*?)</span>', html, re.I | re.S)
        qty_matches = re.findall(r'data-min-qty="([0-9]+)"', html)
        for i, (_, price_html) in enumerate(price_matches[:5]):
            number = re.search(r"([0-9]+,[0-9]+)", price_html)
            if number and i < len(qty_matches):
                thresholds.append((float(qty_matches[i]), parse_number(number.group(1))))
        manufacturer_match = re.search(r"Производитель[^<]{0,300}?([A-Z][A-Za-z0-9 -]{2,30})", html, re.I | re.S)
        manufacturer = manufacturer_match.group(1).strip() if manufacturer_match else ""
        if thresholds:
            price = thresholds[0][1]
        stock_match = re.search(r'<span class="table-list__counter">([0-9\s]+)<span', html)
        if stock_match:
            stock = parse_number(stock_match.group(1))
        moq_match = re.search(r'<span class="hide-sm-mob">Мин:\s*</span>([0-9]+)', html, re.I)
        moq = parse_number(moq_match.group(1)) if moq_match else 1

    if not name:
        raise ValueError("На странице не найдено однозначное название товара")

    return {
        "name": name.strip(),
        "manufacturer": manufacturer.strip(),
        "stock": stock,
        "price": price,
        "currency": currency if price is not None else "н/д",
        "moq": moq,
        "packing": packing,
        "vat": vat,
        "thresholds": thresholds,
    }


def calculate_purchase(required_qty, price, moq=1, packing=1, vat_included=False):
    if price is None:
        return None
    batch = max(required_qty, moq)
    batch = math.ceil(batch / packing) * packing
    rub_price = float(price)
    if not vat_included:
        rub_price *= 1.20
    return batch * rub_price


def unavailable_rows():
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    rows = []
    for item, required in REQUIRED.items():
        for site in SITES:
            rows.append({
                "наименование у поставщика": f"{item} — данные не получены",
                "производитель": "н/д",
                "наличие на складе, шт.": "н/д",
                "цена за штуку при требуемом количестве (с учётом ценовых порогов)": "н/д",
                "минимальная партия": "н/д",
                "кратность упаковки": "н/д",
                "валюта": "н/д",
                "включён ли НДС": "н/д",
                "срок поставки": "н/д",
                "стоимость доставки в Москву": "н/д",
                "минимальная сумма заказа": "н/д",
                "ссылка на страницу": "",
                "дата и время получения данных": now,
            })
    return rows


def read_seed_urls():
    if not SEEDS_FILE.exists():
        return []
    with SEEDS_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        urls = [line.strip() for line in f if line.strip()]
    items = list(REQUIRED.items())
    seeds = []
    for index, url in enumerate(urls):
        item_name, required = items[index % len(items)]
        seeds.append({"url": url, "запрос": item_name, "required": required})
    return seeds


def write_csv(rows):
    with DATA_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = []
    seeds = read_seed_urls()

    for seed in seeds:
        url = seed["url"]
        try:
            parsed = parse_page(url)
            required = seed["required"]
            moq = int(parsed["moq"] or 1)
            packing = int(parsed["packing"] or 1)
            batch = max(required, moq)
            batch = math.ceil(batch / packing) * packing

            effective_price = parsed["price"]
            for threshold_qty, threshold_price in sorted(parsed["thresholds"]):
                if batch >= threshold_qty:
                    effective_price = threshold_price
            if effective_price is not None:
                effective_price = float(effective_price)

            now = datetime.now().astimezone().isoformat(timespec="seconds")
            rows.append({
                "наименование у поставщика": parsed["name"],
                "производитель": parsed["manufacturer"] or "н/д",
                "наличие на складе, шт.": parsed["stock"] if parsed["stock"] is not None else "н/д",
                "цена за штуку при требуемом количестве (с учётом ценовых порогов)":
                    f"{effective_price:.2f}" if effective_price is not None else "н/д",
                "минимальная партия": moq,
                "кратность упаковки": packing,
                "валюта": parsed["currency"],
                "включён ли НДС": parsed["vat"],
                "срок поставки": "н/д",
                "стоимость доставки в Москву": "н/д",
                "минимальная сумма заказа": "н/д",
                "ссылка на страницу": url,
                "дата и время получения данных": now,
            })
        except Exception as exc:
            print(f"Пропущено: {url}: {exc}", file=sys.stderr)

    write_csv(rows)
    print(f"Записано в {DATA_FILE}: {len(rows)} строк")


if __name__ == "__main__":
    main()
