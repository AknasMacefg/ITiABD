import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.csv"
SEEDS_FILE = BASE_DIR / "seeds_url.csv"
REPORT_FILE = BASE_DIR / "comparison_report.md"
OPTIONS_FILE = BASE_DIR / "purchase_options.csv"
CHART_FILE = BASE_DIR / "purchase_costs.svg"

REQUIRED = {
    "ATmega328P-AU": 1,
    "кварцевый резонатор 16 МГц HC-49S": 1,
    "LM358DR": 1,
    "конденсатор керамический 0805 22 пФ C0G 50 В": 2,
    "резистор 0805 1 кОм ±5%": 8,
    "стабилизатор AMS1117-3.3": 1,
    "конденсатор керамический 0805 100 нФ X7R 50 В": 10,
}

CSV_COLUMNS = [
    "вариант",
    "режим",
    "поставщики",
    "позиции",
    "стоимость компонентов, руб.",
    "доставка, руб.",
    "общая стоимость, руб.",
    "максимальный срок, рабочих дней",
    "статус",
]


def read_seeds():
    urls = [
        line.strip()
        for line in SEEDS_FILE.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    names = list(REQUIRED)
    return {url: names[index % len(names)] for index, url in enumerate(urls)}


def number(value):
    match = re.search(r"\d+(?:[.,]\d+)?", str(value or ""))
    return float(match.group(0).replace(",", ".")) if match else None


def supplier(url):
    host = urlparse(url).hostname or ""
    return host.removeprefix("www.")


def load_rows():
    seed_items = read_seeds()
    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    result = []
    for row in rows:
        item = seed_items.get(row.get("ссылка на страницу", ""))
        price_key = next(
            (key for key in row if key.startswith("цена за штуку при требуемом количестве")),
            None,
        )
        if not item or not price_key:
            continue
        price = number(row.get(price_key))
        if price is None or row.get("валюта") != "RUB":
            continue
        result.append({
            "item": item,
            "supplier": supplier(row["ссылка на страницу"]),
            "price": price,
            "delivery": number(row.get("стоимость доставки в Москву")),
            "days": number(row.get("срок поставки")),
            "url": row["ссылка на страницу"],
        })
    return result


def complete_options(rows):
    by_supplier = defaultdict(dict)
    for row in rows:
        by_supplier[row["supplier"]][row["item"]] = row

    options = []
    for name, supplier_rows in by_supplier.items():
        if set(supplier_rows) == set(REQUIRED):
            total = sum(REQUIRED[item] * data["price"] for item, data in supplier_rows.items())
            options.append({
                "mode": "один поставщик",
                "suppliers": name,
                "total": total,
                "days": max(
                    (data["days"] for data in supplier_rows.values() if data["days"] is not None),
                    default=None,
                ),
                "delivery_known": all(data["delivery"] is not None for data in supplier_rows.values()),
            })

    cheapest = {}
    for item in REQUIRED:
        candidates = [row for row in rows if row["item"] == item]
        if candidates:
            cheapest[item] = min(candidates, key=lambda row: row["price"])
    if len(cheapest) == len(REQUIRED):
        suppliers = sorted({row["supplier"] for row in cheapest.values()})
        options.append({
            "mode": "несколько поставщиков",
            "suppliers": ", ".join(suppliers),
            "total": sum(REQUIRED[item] * row["price"] for item, row in cheapest.items()),
            "days": max(
                (row["days"] for row in cheapest.values() if row["days"] is not None),
                default=None,
            ),
            "delivery_known": all(row["delivery"] is not None for row in cheapest.values()),
        })
    return options


def write_chart(options):
    width, height = 900, 520
    left, top, chart_width, chart_height = 230, 55, 610, 380
    max_total = max((option["total"] for option in options), default=1)
    bar_height = 48
    gap = 22
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="450" y="30" text-anchor="middle" font-family="Arial" font-size="20" '
        'font-weight="bold">Стоимость компонентов по вариантам</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" '
        'stroke="#555"/>',
        f'<line x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" '
        f'y2="{top + chart_height}" stroke="#555"/>',
    ]
    for index, option in enumerate(options):
        y = top + index * (bar_height + gap) + 18
        bar_width = option["total"] / max_total * chart_width
        label = f"{option['mode']}: {option['suppliers']}"
        elements.append(
            f'<text x="{left - 10}" y="{y + 30}" text-anchor="end" '
            f'font-family="Arial" font-size="13">{label}</text>'
        )
        elements.append(
            f'<rect x="{left}" y="{y}" width="{bar_width:.2f}" height="{bar_height}" '
            'fill="#3274d9"/>'
        )
        elements.append(
            f'<text x="{left + bar_width + 8:.2f}" y="{y + 30}" '
            f'font-family="Arial" font-size="13">{option["total"]:.2f} руб.</text>'
        )
    elements.append("</svg>")
    CHART_FILE.write_text("\n".join(elements), encoding="utf-8")


def write_outputs(rows, options):
    with OPTIONS_FILE.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for index, option in enumerate(options, start=1):
            delivery = 0 if option["delivery_known"] else "н/д"
            total = option["total"] + delivery if isinstance(delivery, (int, float)) else "н/д"
            writer.writerow({
                "вариант": index,
                "режим": option["mode"],
                "поставщики": option["suppliers"],
                "позиции": len(REQUIRED),
                "стоимость компонентов, руб.": f"{option['total']:.2f}",
                "доставка, руб.": delivery,
                "общая стоимость, руб.": f"{total:.2f}" if isinstance(total, float) else total,
                "максимальный срок, рабочих дней": option["days"] or "н/д",
                "статус": "полные данные" if option["delivery_known"] and option["days"] is not None else "нельзя использовать для итогового выбора",
            })

    write_chart(options)
    cheapest_material = min(options, key=lambda option: option["total"], default=None)
    known_days = [option for option in options if option["days"] is not None]
    under_10 = [option for option in known_days if option["days"] <= 10]
    lines = [
        "# Сравнение вариантов закупки",
        f"Дата формирования: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## График",
        "",
        f"![Стоимость компонентов по вариантам](./{CHART_FILE.name})",
        "",
        "## Результаты",
        "",
        "Методика: стоимость компонентов = сумма (требуемое количество * цена в "
        "[data.csv](./data.csv)).",
        "Доставка и сроки не подставляются. Значение `н/д` исключает вариант из "
        "соответствующего выбора.",
        "",
    ]
    if cheapest_material:
        lines.append(
            f"- Минимальная стоимость компонентов (без подтвержденной доставки): "
            f"{cheapest_material['total']:.2f} руб.; {cheapest_material['mode']}: "
            f"{cheapest_material['suppliers']}."
        )
    else:
        lines.append("- Минимальную стоимость компонентов определить нельзя.")
    lines.append("- Минимальная общая стоимость с доставкой: невозможно определить — "
                 "доставка `н/д`.")
    lines.append(
        "- Минимальный срок поставки: невозможно определить — срок поставки `н/д`."
        if not known_days
        else "- Минимальный срок поставки рассчитан только по строкам с указанным сроком."
    )
    lines.append(
        "- Минимальная стоимость при сроке не более 10 рабочих дней: невозможно "
        "определить — сроки `н/д`."
        if not under_10
        else "- Варианты со сроком не более 10 рабочих дней приведены в "
             "[purchase_options.csv](./purchase_options.csv)."
    )
    lines.extend([
        "",
        "## Сравнение одного и нескольких поставщиков",
        "",
        "Для полного перечня в [data.csv](./data.csv) нет полного набора цен у одного поставщика; "
        "вариант одного поставщика не сформирован.",
        "Раздельная закупка по минимальным ценам компонентов сформирована только "
        "как материальная оценка, без доставки и сроков.",
        "",
        "## Mouser и DigiKey",
        "",
        "API-запрос не выполнялся: ключи API и учетные данные в проекте отсутствуют. "
        "Цены этих поставщиков не выдумывались.",
        "",
        "Подробные строки вариантов: [purchase_options.csv](./purchase_options.csv).",
    ])
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = load_rows()
    options = complete_options(rows)
    write_outputs(rows, options)
    print(f"Созданы {OPTIONS_FILE.name} и {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
