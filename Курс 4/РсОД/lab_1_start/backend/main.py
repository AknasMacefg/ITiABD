import json
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent.parent
ITEMS_PATH = BASE_DIR / "data" / "processed" / "items_normalized.json"


class Item(BaseModel):
    id: int
    name: Optional[str] = None
    category: Optional[str] = None
    value: Optional[float] = None
    updated_at: Optional[str] = None
    active: Optional[bool] = None


class ItemInput(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    value: Optional[float] = None
    updated_at: Optional[str] = None
    active: Optional[bool] = None


def load_items() -> Dict[int, Item]:
    with ITEMS_PATH.open(encoding="utf-8") as file:
        records = json.load(file)
    return {record["id"]: Item(**record) for record in records}


items: Dict[int, Item] = load_items()
app = FastAPI(title="Items учебный backend")


@app.get("/api/items", response_model=List[Item])
def list_items() -> List[Item]:
    return [items[item_id] for item_id in sorted(items)]


@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemInput) -> Item:
    item_id = payload.id
    if item_id is None:
        item_id = max(items, default=0) + 1
    if item_id in items:
        raise HTTPException(status_code=409, detail="Item with this id already exists")

    item = Item(id=item_id, **payload.dict(exclude={"id"}))
    items[item_id] = item
    return item


@app.put("/api/items/{item_id}", response_model=Item)
def replace_item(item_id: int, payload: ItemInput) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    item = Item(id=item_id, **payload.dict(exclude={"id"}))
    items[item_id] = item
    return item


@app.patch("/api/items/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemInput) -> Item:
    current = items.get(item_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Item not found")

    values = current.dict()
    values.update(payload.dict(exclude_unset=True, exclude={"id"}))
    values["id"] = item_id
    item = Item(**values)
    items[item_id] = item
    return item


@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Response:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


DYNAMIC_PAGE = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Динамические данные</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; }
    table { border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #bbb; padding: .45rem .7rem; text-align: left; }
    th { background: #eee; }
    .controls { display: flex; gap: .7rem; align-items: center; }
  </style>
</head>
<body>
  <h1>Товары</h1>
  <div class="controls">
    <button id="load-button" type="button">Загрузить данные</button>
    <label>Категория:
      <select id="category-filter">
        <option value="">Все</option>
      </select>
    </label>
  </div>
  <p id="status">Данные еще не загружены.</p>
  <table>
    <thead><tr><th>ID</th><th>Название</th><th>Категория</th><th>Значение</th><th>Активен</th></tr></thead>
    <tbody id="items-body"></tbody>
  </table>
  <script>
    let items = [];
    const body = document.getElementById('items-body');
    const filter = document.getElementById('category-filter');
    const statusText = document.getElementById('status');

    function render() {
      const category = filter.value;
      body.innerHTML = items
        .filter(item => !category || item.category === category)
        .map(item => `<tr><td>${item.id}</td><td>${item.name ?? ''}</td>` +
          `<td>${item.category ?? ''}</td><td>${item.value ?? ''}</td>` +
          `<td>${item.active ? 'Да' : 'Нет'}</td></tr>`).join('');
    }

    async function loadItems() {
      statusText.textContent = 'Загрузка...';
      const response = await fetch('/api/items');
      items = await response.json();
      const categories = [...new Set(items.map(item => item.category).filter(Boolean))];
      filter.innerHTML = '<option value="">Все</option>' +
        categories.map(category => `<option value="${category}">${category}</option>`).join('');
      render();
      statusText.textContent = `Загружено записей: ${items.length}`;
    }

    document.getElementById('load-button').addEventListener('click', loadItems);
    filter.addEventListener('change', render);
    window.addEventListener('load', loadItems);
  </script>
</body>
</html>"""


@app.get("/dynamic", response_class=HTMLResponse)
def dynamic_page() -> str:
    return DYNAMIC_PAGE