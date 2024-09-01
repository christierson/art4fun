import html
import re
from product import Product, Warehouse

with open("Lagerlista.html", "r") as fp:
    document = fp.read()
document = document.split("<body>")[1]
document = document.split("</body>")[0]
document = document.split('<table width="100%">')

w = Warehouse()

for a in document[3:-1]:
    b = a.replace("\n", "").replace("\t", "").replace(" ", "")
    b = [html.unescape(i) for i in re.split(r"<[^>]*>", b) if i]
    id, label, index, stock_warning, in_stock, cost, value = b
    index = int(index)
    stock_warning = int(stock_warning[:-3])
    in_stock = int(in_stock[:-3])
    cost = float(cost.replace(",", "."))
    value = float(value.replace(",", "."))

    p = Product(id, label, index, stock_warning, in_stock, cost, value)
    w.new_product(p)


with open("Artikelstatistik.html", "r") as fp:
    document = fp.read()
document = document.split("<body>")[1]
document = document.split("</body>")[0]

document = document.split('<table width="100%" border="0" class="nospacing">')
for a in document[2:]:
    b = a.replace("\n", "").replace("\t", "").replace(" ", "")
    b = [html.unescape(i) for i in re.split(r"<[^>]*>", b) if i]
    id, label, amount, total, _, _ = b
    amount = float(amount.replace(" ", "").replace(",", "."))
    total = float(total.replace(" ", "").replace(",", "."))
    print(id, label, amount, total)
