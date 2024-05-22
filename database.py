import datetime

class Company:
    def __init__(self, company_code: str, name: str):
        self.company_code = company_code
        self.name = name

class Category:
    def __init__(self, category_code: str, name: str):
        self.category_code = category_code
        self.name = name  

class Product:
    def __init__(self, product_code: str, name: str, purchase_cost: float, selling_price: float, quantity, quantity_limit, company: Company, category: Category):
        self.product_code = product_code
        self.name = name
        self.purchase_cost = purchase_cost
        self.selling_price = selling_price
        self.quantity = quantity
        self.quantity_limit = quantity_limit

class DrugBatch:
    def __init__(self, batch_code: str, quantity: int, expiration_date: datetime):
        self.batch_code = batch_code
        self.quantity = quantity
        self.expiration_date = expiration_date
    
class Drug(Product):
    def __init__(self, product_code: str, name: str, purchase_cost: float, selling_price: float, quantity, quantity_limit, quality: bool, batches: list):
        super().__init__(product_code, name, purchase_cost, selling_price, quantity, quantity_limit)
        self.quality = quality
        self.batches = batches
 
class UserPermissions:
    def __init__(self):
        self.view_stock = False
        self.edit_stock = False
        self.add_products = False
        self.view_notifications = False
        self.create_client_list = False
        self.view_orders = False
        self.add_orders = False
        self.change_order_state = False
        self.create_bills = False
        self.view_salaries = False
        self.user_administration = False

class User:
    # TODO: Define id type
    def __init__(self, id, username: str, password: str, full_name: str, permissions: UserPermissions):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.permissions = permissions
