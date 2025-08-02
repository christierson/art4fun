from openpyxl import Workbook

workbook = Workbook()
sheet = workbook.active
all_products = {}


with open(stock_list, "r", encoding='latin-1') as fp:
    document = fp.read()

document = document.split("-------------------------")[1]
document = document.strip().split("\n")

for article in document:
    a = article.replace(" ", "").replace(",", ".")
    a = a.strip().split("\t")
    id, label, _, _, in_stock, _, _ = a
    in_stock = float(in_stock)
    all_products[id] = {"label": label, "in_stock": in_stock}


with open(product_statistics, "r", encoding='latin-1') as fp:
    document = fp.read()

document = document.split("-------------------------")[1]
document = document.strip().split("\n")
found = []
not_found = []
products = {}
for article in document:
    a = article.replace(" ", "").replace(",", ".")
    a = a.strip().split("\t")
    if len(a) != 5:
        continue
    id, label, _, sold, _ = a
    if id not in all_products:
        continue
    found.append(id)
    products[id] = all_products[id]
    products[id]["sold"] = sold

sheet[f"A1"] = "id"
sheet[f"B1"] = "label"
sheet[f"C1"] = "in_stock"
sheet[f"D1"] = "sold"
for i, (id, product) in enumerate(products.items()):
    sheet[f"A{i+2}"] = id
    sheet[f"B{i+2}"] = product["label"]
    sheet[f"C{i+2}"] = product["in_stock"]
    sheet[f"D{i+2}"] = product["sold"]

workbook.save(filename="output.xlsx")
