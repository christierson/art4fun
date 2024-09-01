class Product:
    def __init__(self, id, label, index, stock_warning, in_stock, cost, value):
        self.id = id
        self.label = label
        self.index = index
        self.stock_warning = stock_warning
        self.in_stock = in_stock
        self.cost = cost
        self.value = value

    def __str__(self):
        return self.label

class Warehouse:
    def __init__(self):
        self.products = {}

    def new_product(self, product:Product):
        if product.id in self.products:
            raise Exception(f"Product with id {product.id} is already registered")
        self.products[product.id] = product

    def __str__(self):
        return f"Warehouse conaining {len(self.products)} products"