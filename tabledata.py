from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog
import json
import string

COLUMNS = [a for a in string.ascii_uppercase]


class TableData:
    def __init__(self):
        self.data = {}

    def save_table(self):

        workbook = Workbook()
        sheet = workbook.active

        cols = set([label for item in self.data.values() for label in item.keys()])
        for i, col in enumerate(cols):
            sheet[f"{COLUMNS[i]}1"] = col

        for i, (key, value) in enumerate(self.data.items()):
            for j, col in enumerate(cols):
                cell = f"{COLUMNS[j]}{i+2}"
                sheet[cell] = value.get(col)

        workbook.save(filename="output.xlsx")

    def read_table(self, path, id_col, cols):
        with open(path, "r", encoding="latin-1") as fp:
            document = fp.read()

        head, data, footer = document.split("-------------------------")
        head = head.strip().split("\n")[-1].split("\t")
        head = [h.strip().lower() for h in head]

        col_ids = [col.strip().lower() for col in cols.keys()]
        col_labels = cols.values()
        id_col = id_col.lower()

        if any([col not in head for col in col_ids]):
            print(f"Could not read file {path} - Column mismatch")
            print(f"Requested cols: {cols.keys()}")
            print(f"Available cols: {head}")
            return

        if id_col not in head:
            print(f"Could not read file {path} - No id column found")
            print(f"Requested id: {id_col}")
            print(f"Available cols: {head}")

        id_index = head.index(id_col)
        col_indexes = [head.index(col) for col in col_ids]
        keys = cols.values()
        print(col_indexes)
        print(keys)
        data = data.strip().split("\n")
        for article in data:
            item_data = article.strip().split("\t")
            if len(item_data) != len(head):
                continue
            id = item_data[id_index].strip()
            values = [item_data[i].strip() for i in col_indexes]
            data = dict(zip(keys, values))
            if id in self.data:
                self.data[id].update(data)
                print("UPDATE")
            else:
                print("NEW ENTRY")
                self.data[id] = data


t = TableData()

t.read_table(
    path="Lagerlista.txt",
    id_col="Artikelnr",
    cols={
        "Benämning": "Benämning",
        "Antal i lager": "I lager",
    },
)
t.read_table(
    path="Artikelstatistik.txt",
    id_col="Art.nr",
    cols={
        "Antal": "Sålt",
    },
)


print({key: value for key, value in t.data.items() if len(value) == 3})
t.save_table()
