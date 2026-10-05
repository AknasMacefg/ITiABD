import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd
from babel import Locale


INPUT_FILE = Path(__file__).with_name("data_all.csv")
OUTPUT_FILE = Path(__file__).with_name("data_all_cleaned.csv")

COUNTRY_ALIASES = {
	"usa": "США",
	"united states": "США",
	"united states of america": "США",
	"сша": "США",
	"uk": "Великобритания",
	"united kingdom": "Великобритания",
	"great britain": "Великобритания",
	"великобритания": "Великобритания",
	"canada": "Канада",
	"канада": "Канада",
	"brazil": "Бразилия",
	"бразилия": "Бразилия",
	"china": "Китай",
	"китай": "Китай",
	"hong kong": "Гонконг",
	"hong kong sar china": "Гонконг",
	"japan": "Япония",
	"япония": "Япония",
	"germany": "Германия",
	"германия": "Германия",
	"france": "Франция",
	"франция": "Франция",
	"italy": "Италия",
	"италия": "Италия",
	"spain": "Испания",
	"испния": "Испания",
	"испания": "Испания",
	"netherlands": "Нидерланды",
	"the netherlands": "Нидерланды",
	"нидерланды": "Нидерланды",
	"switzerland": "Швейцария",
	"швейцария": "Швейцария",
	"australia": "Австралия",
	"австралия": "Австралия",
	"sweden": "Швеция",
	"швеция": "Швеция",
	"finland": "Финляндия",
	"финляндия": "Финляндия",
	"denmark": "Дания",
	"дания": "Дания",
	"poland": "Польша",
	"польша": "Польша",
	"portugal": "Португалия",
	"португалия": "Португалия",
	"austria": "Австрия",
	"австрия": "Австрия",
	"belgium": "Бельгия",
	"бельгия": "Бельгия",
	"greece": "Греция",
	"греция": "Греция",
	"norway": "Норвегия",
	"норвегия": "Норвегия",
	"czech republic": "Чехия",
	"czechia": "Чехия",
	"чехия": "Чехия",
	"turkey": "Турция",
	"тюркия": "Турция",
	"турция": "Турция",
	"ireland": "Ирландия",
	"ирландия": "Ирландия",
	"south korea": "Южная Корея",
	"republic of korea": "Южная Корея",
	"южная корея": "Южная Корея",
	"india": "Индия",
	"индия": "Индия",
	"mexico": "Мексика",
	"мексика": "Мексика",
	"argentina": "Аргентина",
	"аргентина": "Аргентина",
	"chile": "Чили",
	"чили": "Чили",
	"colombia": "Колумбия",
	"колумбия": "Колумбия",
	"peru": "Перу",
	"перу": "Перу",
	"vietnam": "Вьетнам",
	"вьетнам": "Вьетнам",
	"indonesia": "Индонезия",
	"индонезия": "Индонезия",
	"malaysia": "Малайзия",
	"малайзия": "Малайзия",
	"thailand": "Таиланд",
	"тайланд": "Таиланд",
	"singapore": "Сингапур",
	"сингапур": "Сингапур",
	"united arab emirates": "ОАЭ",
	"uae": "ОАЭ",
	"оаэ": "ОАЭ",
	"saudi arabia": "Саудовская Аравия",
	"саудовская аравия": "Саудовская Аравия",
	"south africa": "Южная Африка",
	"юар": "Южная Африка",
	"russia": "Россия",
	"россия": "Россия",
	"ukraine": "Украина",
	"украина": "Украина",
	"kazakhstan": "Казахстан",
	"казахстан": "Казахстан",
	"belarus": "Беларусь",
	"беларусь": "Беларусь",
	"romania": "Румыния",
	"румыния": "Румыния",
	"bulgaria": "Болгария",
	"болгария": "Болгария",
	"croatia": "Хорватия",
	"хорватия": "Хорватия",
	"serbia": "Сербия",
	"сербия": "Сербия",
	"slovakia": "Словакия",
	"словакия": "Словакия",
	"hungary": "Венгрия",
	"венгрия": "Венгрия",
}

MISSING_VALUES = {"", "-", "нет данных", "нет значения", "неизвестно", "unknown", "none", "null", "n/a", "na"}

INDUSTRY_ALIASES = {
	"banks": "Банковское дело",
	"banking": "Банковское дело",
	"financial services": "Финансовые услуги",
	"finance": "Финансовые услуги",
	"real estate": "Недвижимость",
	"telecommunications": "Телекоммуникации",
	"telecommunication services": "Телекоммуникации",
	"energy": "Энергетика",
	"software": "Программное обеспечение",
	"healthcare": "Здравоохранение",
	"pharmaceuticals": "Фармацевтика",
	"retail": "Розничная торговля",
	"insurance": "Страхование",
	"investment": "Инвестиции",
	"oil and gas": "Нефтегазовая промышленность",
	"manufacturing": "Производство",
	"food and beverages": "Пищевая промышленность",
}


def build_country_translations():
	english = Locale("en").territories
	russian = Locale("ru").territories
	translations = {
		name.casefold(): russian[code]
		for code, name in english.items()
		if code in russian and name and russian[code]
	}
	translations.update(COUNTRY_ALIASES)
	return translations


COUNTRY_TRANSLATIONS = build_country_translations()
KNOWN_RUSSIAN_COUNTRIES = {
	value.casefold(): value for value in COUNTRY_TRANSLATIONS.values()
}


def normalize_country(value):
	normalized = " ".join(str(value or "").split())
	key = normalized.casefold()
	if key in MISSING_VALUES:
		return None
	return COUNTRY_TRANSLATIONS.get(key) or KNOWN_RUSSIAN_COUNTRIES.get(key)


def parse_number(value):
	value = value.replace(" ", "").replace("\u00a0", "")
	if "," in value and "." in value:
		if value.rfind(",") > value.rfind("."):
			value = value.replace(".", "").replace(",", ".")
		else:
			value = value.replace(",", "")
	elif "," in value:
		value = value.replace(",", ".")
	return Decimal(value)


def normalize_capitalization(value):
	text = " ".join(str(value or "").split())
	if text.casefold() in MISSING_VALUES:
		return None

	currency_match = re.search(r"(?:US)?\$|R\$|€|£|¥", text)
	currency = currency_match.group(0) if currency_match else "$"
	number_match = re.search(r"[\d.,\s\u00a0]+", text)
	if not number_match:
		return None

	try:
		amount = parse_number(number_match.group(0))
	except InvalidOperation:
		return None

	suffix = text[number_match.end():].casefold()
	if re.search(r"(?:b|bn|billion|млрд)", suffix):
		amount *= Decimal("1000000000")
	elif re.search(r"(?:m|mn|million|млн)", suffix):
		amount *= Decimal("1000000")
	elif re.search(r"(?:k|thousand|тыс)", suffix):
		amount *= Decimal("1000")

	if amount >= Decimal("1000000000"):
		amount /= Decimal("1000000000")
		unit = "B"
	elif amount >= Decimal("1000000"):
		amount /= Decimal("1000000")
		unit = "M"
	elif amount >= Decimal("1000"):
		amount /= Decimal("1000")
		unit = "K"
	else:
		unit = ""

	formatted = format(amount.quantize(Decimal("0.01")), "f").rstrip("0").rstrip(".")
	return f"{currency}{formatted}{f' {unit}' if unit else ''}"


def normalize_industry(value):
	normalized = " ".join(str(value or "").split())
	if normalized.casefold() in MISSING_VALUES:
		return None

	normalized = re.sub(r"\s*[-–—]\s*", " — ", normalized)
	key = normalized.casefold()
	if key in INDUSTRY_ALIASES:
		return INDUSTRY_ALIASES[key]
	return normalized[:1].upper() + normalized[1:]


def clean_data(dataframe):
	country_column = "СТРАНА"
	capitalization_column = "КАПИТАЛИЗАЦИЯ"
	industry_column = "ОТРАСЛЬ"
	dataframe[country_column] = dataframe[country_column].map(normalize_country)
	dataframe = dataframe[dataframe[country_column].notna()].copy()
	dataframe[capitalization_column] = dataframe[capitalization_column].map(normalize_capitalization)
	dataframe = dataframe[dataframe[capitalization_column].notna()].copy()
	dataframe[industry_column] = dataframe[industry_column].map(normalize_industry)
	dataframe = dataframe.drop_duplicates().reset_index(drop=True)
	return dataframe


def read_data():
	with INPUT_FILE.open(encoding="utf-8-sig", newline="") as file:
		rows = list(csv.reader(file))

	header = rows[0]
	fixed_rows = []
	for row in rows[1:]:
		if len(row) == 5:
			row = [row[0], row[1], "", row[2], row[3], row[4]]
		elif len(row) > len(header):
			row = row[:3] + [",".join(row[3:-2])] + row[-2:]
		fixed_rows.append(row + [""] * (len(header) - len(row)))
	return pd.DataFrame(fixed_rows, columns=header)


def main():
	dataframe = read_data()
	cleaned = clean_data(dataframe)
	cleaned.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
	print(f"Сохранено строк: {len(cleaned)}")
	print(f"Файл: {OUTPUT_FILE.name}")


if __name__ == "__main__":
	main()
