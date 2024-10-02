from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog
from tabledata import TableData
import json

COLUMNS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "X",
    "Y",
    "Z",
]

workbook = Workbook()
sheet = workbook.active

with open("config.json", "r") as fp:
    config = json.load(fp)
table = TableData(id_cols=config["id_cols"], cols=config["data"])

with open("LagerLista.txt", "r", encoding="latin-1") as fp:
    document = fp.read()

head, data, footer = document.split("-------------------------")
head = head.strip().split("\n")[-1].split("\t")

data = data.strip().split("\n")
for article in data:
    item_data = article.replace(" ", "").replace(",", ".")
    item_data = item_data.strip().split("\t")
    table.add(dict(zip(head, item_data)))

with open("Artikelstatistik.txt", "r", encoding="latin-1") as fp:
    document = fp.read()

head, data, footer = document.split("-------------------------")
head = head.strip().split("\n")[-1].split("\t")

data = data.strip().split("\n")
for article in data:
    item_data = article.replace(" ", "").replace(",", ".")
    item_data = item_data.strip().split("\t")
    table.add(dict(zip(head, item_data)))


data = table.get()


def save_table(table):
    cols = set()
    for id, item in table.items():
        cols = cols.union(set(item.keys()))
    cols = list(cols)
    for i, col in enumerate(cols):
        sheet[f"{COLUMNS[i]}1"] = col

    for i, (key, value) in enumerate(table.items()):
        for j, col in enumerate(cols):
            cell = f"{COLUMNS[j]}{i+2}"
            sheet[cell] = value.get(col)


save_table(data)
print(data)
workbook.save(filename="output.xlsx")
