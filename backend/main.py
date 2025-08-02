from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from openpyxl import Workbook

from io import BytesIO

app = FastAPI()

# optional CORS if no proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_result_sheet(inventory, subtractions):
    workbook = Workbook()
    sheet = workbook.active
    result = {}
    for id, sold in subtractions.items():
        if id not in inventory:
            continue
        result[id] = {**inventory[id], "sold": sold}

    sheet[f"A1"] = "id"
    sheet[f"B1"] = "label"
    sheet[f"C1"] = "in_stock"
    sheet[f"D1"] = "sold"
    for i, (id, product) in enumerate(result.items()):
        sheet[f"A{i+2}"] = id
        sheet[f"B{i+2}"] = product["label"]
        sheet[f"C{i+2}"] = product["in_stock"]
        sheet[f"D{i+2}"] = product["sold"]

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
        id, _, _, sold, _ = line
        products[id] =  sold
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

@app.post("/api/upload")
async def upload_file(inventory: UploadFile = File(...), subtractions: UploadFile = File(...)):
    inventory = await parse_file(inventory)
    subtractions = await parse_file(subtractions)

    inventory = parse_inventory_file(inventory)
    subtractions = parse_subtractions_file(subtractions)

    sheet = generate_result_sheet(inventory, subtractions)
    
    buffer = BytesIO()
    sheet.save(buffer)
    buffer.seek(0)


    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=result.xlsx"}
    )