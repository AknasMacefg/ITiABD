# Лабораторная работа №3

Парсинг веб-страниц и мультипроцессинг: `requests + BeautifulSoup`,
Scrapy, `ThreadPoolExecutor`, `multiprocessing.Pool`,
`ProcessPoolExecutor` и интеграция с витриной лабораторной II.

## Структура

```text
lab_3/
├── README.md
├── requirements.txt
├── lab_3.ipynb
├── src/
│   ├── bs_scraper.py         # реализация BeautifulSoup
│   ├── catalog_spider.py     # реализация Scrapy
│   ├── benchmark_io.py       # сетевой benchmark
│   └── benchmark_cpu.py      # CPU benchmark
├── data/
│   ├── raw/
│   └── processed/
└── results/
```

## Установка и окружение

Проверенное окружение: Python 3.13.2, requests 2.32.5, beautifulsoup4
4.13.3, lxml 6.1.3, Scrapy 2.18.0, pandas 2.3.2, matplotlib 3.10.0.

```powershell
python -m pip install -r .\requirements.txt
```

## Запуск учебного стенда

Все команды выполняются из каталога `lab_3`:

```powershell
Учебный стенд каталога находится в `site/`; его URL:
`http://127.0.0.1:8765/index.html`.
```

Сервер открывает `http://127.0.0.1:8765/index.html`. Вторую команду
оставьте выполняться в отдельном окне PowerShell.

## Скраперы

```powershell
python .\src\bs_scraper.py --start-url http://127.0.0.1:8765/index.html
scrapy runspider .\src\catalog_spider.py `
  -a start_url=http://127.0.0.1:8765/index.html `
  -O .\data\raw\catalog_scrapy.jsonl
```

Результаты: `data/raw/catalog_bs.csv`,
`data/raw/catalog_scrapy.jsonl` и `results/scraping_errors.csv`.

## Проверка и очистка

Очищенный результат и `quality_report.csv` уже сохранены в комплекте. Для
повторной проверки используются assert-проверки из ноутбука и сравнение
общих `org_id` в отчёте.

Очищенный файл — `data/processed/catalog_clean.csv`, протокол проверок —
`results/quality_report.csv`.

## Benchmarks

Сетевой I/O benchmark использует только локальный сервер:

```powershell
python .\src\benchmark_io.py --base-url http://127.0.0.1:8765/ --repeat 2 --runs 3
```

CPU benchmark:

```powershell
python .\src\benchmark_cpu.py --input .\data\processed\catalog_clean.csv `
  --fragments 200 --runs 3
```

## Обогащение витрины

Обогащённая витрина `data/processed/data_mart_web.csv`, протокол
и график `results/reports_by_sector.png` сохранены в комплекте.

Полный текст выводов и интерпретация результатов находятся в
[`results/report.md`](results/report.md).
Ответы на контрольные вопросы находятся в
[`results/control_questions.md`](results/control_questions.md).
