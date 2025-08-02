from openpyxl import Workbook
import json
import string

COLUMNS = [a for a in string.ascii_uppercase]


class TableData:
    def __init__(self):
        self.data = {}
        self.cols = set()
        self.files = {}

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

    def filter_incomplete(self):
        num_cols = max([len(props) for props in self.data.values()])
        self.data = {
            key: value for key, value in self.data.items() if len(value) == num_cols
        }
        print("Removed incomplete rows")

    def read_table(self, path):
        with open(path, "r", encoding="latin-1") as fp:
            document = fp.read()
        head, table, footer = document.split("-------------------------")
        head = head.strip().split("\n")[-1].split("\t")
        head = [h.strip().lower() for h in head]
        table = table.strip().split("\n")
        data = []
        for row in table:
            row_data = row.strip().split("\t")
            if len(row_data) == len(head):
                data.append([value.strip() for value in row_data])
        self.files[path] = {"cols": head, "data": data}

    def _read_table(self, path, id_col, cols):
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


class FileTable:
    def __init__(self):
        self.data = []
        self.cols = []

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

    def filter_incomplete(self):
        num_cols = max([len(props) for props in self.data.values()])
        self.data = {
            key: value for key, value in self.data.items() if len(value) == num_cols
        }
        print("Removed incomplete rows")

    def read_table(self, path):
        with open(path, "r", encoding="latin-1") as fp:
            document = fp.read()
        head, table, footer = document.split("-------------------------")
        head = head.strip().split("\n")[-1].split("\t")
        head = [h.strip().lower() for h in head]

        self.cols = head
        for row in table.strip().split("\n"):
            row_data = row.strip().split("\t")
            if len(row_data) != len(head):
                continue
            self.data.append({col: row_data[i].strip() for i, col in enumerate(head)})
