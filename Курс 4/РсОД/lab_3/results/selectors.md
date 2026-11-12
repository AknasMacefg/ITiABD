# Этап A. Структура учебного каталога

## Ресурс

- Базовый URL: `http://127.0.0.1:8765/`
- Каталог: `index.html`, `index_2.html`, ...
- Профиль организации: `organizations/{org_id}.html`
- Формат ответа страниц: `text/html; charset=utf-8`

Каталог генерируется скриптом [`make_catalog.py`](../make_catalog.py) из
`organizations.csv`. На каждой странице каталога размещается не более четырех
карточек.

## CSS-селекторы

| Данные | Страница | Селектор/признак | Примечание |
|---|---|---|---|
| Идентификатор | каталог | `article.org-card[data-org-id]` | значение атрибута `data-org-id` |
| Название | каталог | `article.org-card .org-name` | текст заголовка карточки |
| Сектор | каталог и профиль | `.sector` | текст сектора |
| Ссылка на профиль | каталог | `a.profile-link[href]` | относительная ссылка |
| Следующая страница | каталог | `a.next-page[href]` | отсутствует на последней странице |
| Идентификатор профиля | профиль | `main.org-profile[data-org-id]` | значение атрибута |
| Количество публикаций | профиль | `.reports-count` | неотрицательное целое |
| Дата обзора | профиль | `.last-reviewed` | ISO `YYYY-MM-DD` |
| Описание | профиль | `.description` | текстовое поле |

## `robots.txt`

Файл доступен по адресу `http://127.0.0.1:8765/robots.txt` и содержит:

```text
User-agent: *
Allow: /
Disallow: /private/
```

Для учебного каталога разрешен обход всех опубликованных страниц; путь
`/private/` обходить нельзя. Наличие `robots.txt` не отменяет условий
использования внешнего сайта: дополнительно нужно соблюдать его правила,
частоту запросов, лимиты и запрет на сбор персональных данных.

## Первый HTTP-запрос

Проверка выполняется после запуска сервера:

```powershell
python .\make_catalog.py --input .\organizations.csv --out .\site
python .\delay_server.py --dir .\site --port 8765 --delay 0.12
```

Для фиксации `status_code`, `Content-Type`, размера и времени ответа используйте
`requests.get("http://127.0.0.1:8765/index.html", timeout=10)` и сохраните
полученные значения в отчет лабораторной работы.

## Этапы B–C

Запуск BeautifulSoup-скрапера из корня лабораторной:

```powershell
python .\src\bs_scraper.py --start-url http://127.0.0.1:8765/index.html
```

Он сохраняет записи в `data/raw/catalog_bs.csv`, а ошибки и предупреждения —
в `results/scraping_errors.csv`. Для HTTP 404 используется отдельная запись
`error_type=http_error`, после чего обход продолжается. Повторный `org_id`
получает `error_type=duplicate_card`; циклическая пагинация блокируется
множеством `visited_urls`.

Запуск независимого Scrapy Spider:

```powershell
scrapy runspider .\src\catalog_spider.py `
  -a start_url=http://127.0.0.1:8765/index.html `
  -O .\data\raw\catalog_scrapy.jsonl
```

Spider соблюдает `robots.txt`, использует один запрос к домену за раз,
задержку `0.25` секунды и AutoThrottle. Ошибки Scrapy сохраняются в
`results/scraping_errors.csv`.

Сравнение результатов:

```powershell
```

Сравнение ключей двух реализаций отражено в `results/quality_report.csv`;
на текущем каталоге обе реализации получили одинаковый набор из 10 уникальных
ключей.
