from fastapi import FastAPI, Request
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openpyxl import Workbook
import uvicorn
from io import BytesIO
import os
import json
import webbrowser
import threading

app = FastAPI()




# optional CORS if no proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_result_sheet(inventory):
    workbook = Workbook()
    sheet = workbook.active
    sheet[f"A1"] = "id"
    sheet[f"B1"] = "label"
    sheet[f"C1"] = "in_stock"
    sheet[f"D1"] = "sold"
    for i, (id, product) in enumerate(inventory.items()):
        sheet[f"A{i+2}"] = id
        sheet[f"B{i+2}"] = product.get("label")
        sheet[f"C{i+2}"] = product.get("in_stock")
        sheet[f"D{i+2}"] = product.get("sold")

    return workbook

    
def parse_inventory_file(inventory):
    products = {}
    for line in inventory:
        id, label, _, _, in_stock, _, _ = line
        in_stock = float(in_stock)
        products[id] = {"label": label, "in_stock": in_stock}
    return products

def parse_subtractions_file(subtractions):
    products = {}
    for line in subtractions:
        if len(line) != 5:
            continue
        id, label, _, sold, _ = line
        products[id] = {"label": label, "sold": sold}
    return products

async def parse_file(file):
    document = await file.read()
    document = document.decode("latin1")
    document = document.split("-------------------------")[1]
    document = document.strip().split("\n")
    parsed = []
    for article in document:
        a = article.replace(" ", "").replace(",", ".")
        a = a.strip().split("\t")
        parsed.append(a)
    return parsed


@app.post("/api/inventory")
async def upload_inventory(inventory: UploadFile = File(...)):
    inventory = await parse_file(inventory)
    inventory = parse_inventory_file(inventory)
    with open("products.json", 'r') as fp:
        products = json.load(fp)

    result = {**products}
    for id, data in inventory.items():
        if id in products:
            result[id] = {
                **products[id],
                **data
            }
        else:
            result[id] = data
    with open("products.json", 'w') as fp:
        json.dump(result, fp)
    return "OK"




@app.post("/api/subtractions")
async def upload_subractions(subtractions: UploadFile = File(...)):
    subtractions = await parse_file(subtractions)
    subtractions = parse_subtractions_file(subtractions)
    with open("products.json", 'r') as fp:
        products = json.load(fp)
    result = {**products}
    for id, data in subtractions.items():
        if id in products:
            result[id] = {
                **products[id],
                **data
            }
        else:
            result[id] = data
    with open("products.json", 'w') as fp:
        json.dump(result, fp)
    return "OK"


@app.post("/api/calculate")
async def calculate(request: Request):
    data = await request.json()
    onlyComplete = data.get("onlyComplete")
    with open("products.json", 'r') as fp:
        products = json.load(fp)
    with open("filters.json", "r") as fp:
        filters = json.load(fp)
    if filters:
        products = {id: data for id, data in products.items() if any([id.startswith(filter) for filter in filters])}
    if onlyComplete:
        products = {id: data for id, data in products.items() if all(key in data for key in ["in_stock", "sold"])}
    sheet = generate_result_sheet(products)
    
    buffer = BytesIO()
    sheet.save(buffer)
    buffer.seek(0)


    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=result.xlsx"}
    )


@app.get("/api/filters")
async def get_filters():
    if not os.path.exists("filters.json"):
        with open("filters.json", "w") as fp:
            json.dump([], fp)
    with open("filters.json", "r") as fp:
        filters = json.load(fp)

    return JSONResponse(filters)

@app.post("/api/filters")
async def set_filters(request: Request):
    data = await request.json()
    filters = data.get("filters")
    if filters is None:
        return "INVALID"

    with open("filters.json", "w") as fp:
        json.dump(filters, fp)
    
    return JSONResponse(filters)


@app.get("/api/clear")
async def clear():

    with open("products.json", "w") as fp:
        json.dump({}, fp)
    
    return {"message": "ready"}

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("frontend/dist/index.html")

def open_browser():
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)