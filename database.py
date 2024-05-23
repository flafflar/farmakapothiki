import datetime
import sqlite3
import typing
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
    def __init__(self, id: int, username: str, password: str, full_name: str, permissions: UserPermissions):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.permissions = permissions

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        
    def create_tables(self):
        # Create User table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS User (
                Id INTEGER PRIMARY KEY,
                Username TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Fullname TEXT NOT NULL
            )
        ''')
        
        # Create UserPermissions table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS UserPermissions (
                UserId INTEGER NOT NULL,
                ViewStock INTEGER NOT NULL,
                EditStock INTEGER NOT NULL,
                AddProduct INTEGER NOT NULL,
                ViewNotifications INTEGER NOT NULL,
                CreateClientList INTEGER NOT NULL,
                ViewOrders INTEGER NOT NULL,
                AddOrders INTEGER NOT NULL,
                ChangeOrderState INTEGER NOT NULL,
                ViewBills INTEGER NOT NULL,
                CreateBills INTEGER NOT NULL,
                ViewSalaries INTEGER NOT NULL,
                UserAdministration INTEGER NOT NULL,
                PRIMARY KEY (UserId),
                FOREIGN KEY (UserId) REFERENCES User(Id)
            )
        ''')
        
        # Create Company table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Company (
                CompanyCode INTEGER PRIMARY KEY,
                Name TEXT NOT NULL
            )
        ''')
        
        # Create Category table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Category (
                CategoryCode INTEGER PRIMARY KEY,
                Name TEXT NOT NULL
            )
        ''')
        
        # Create Product table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                ProductCode INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                PurchaseCost REAL NOT NULL,
                SellingPrice REAL NOT NULL,
                Quantity INTEGER NOT NULL,
                QuantityLimit INTEGER NOT NULL,
                CompanyCode INTEGER,
                CategoryCode INTEGER,
                FOREIGN KEY (CompanyCode) REFERENCES Company(CompanyCode),
                FOREIGN KEY (CategoryCode) REFERENCES Category(CategoryCode)
            )
        ''')
        
        # Create Drug table
        self.c.execute('''
                    CREATE TABLE IF NOT EXISTS Drug (
                        ProductCode INTEGER PRIMARY KEY,
                        Quality INTEGER,
                        FOREIGN KEY (ProductCode) REFERENCES Product(ProductCode)
                    )
                ''')
        
        # Create DrugBatch table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS DrugBatch (
                BatchCode INTEGER PRIMARY KEY,
                ProductCode INTEGER,
                Quantity INTEGER NOT NULL,
                ExpirationDate TEXT NOT NULL,
                FOREIGN KEY (ProductCode) REFERENCES Product(ProductCode)
            )
        ''')
        
        # Commit the changes and close the connection
        self.conn.commit()
        self.conn.close()

    def get_all_users(self) -> list[User]:
        self.c.execute('SELECT * FROM User')
        users = []
        for row in self.c.fetchall():
            self.c.execute('SELECT * FROM UserPermissions WHERE UserId = ?', (row[0],))
            perm_row = self.c.fetchone()
            if perm_row:
                permissions = UserPermissions(
                    view_stock=bool(perm_row[1]),
                    edit_stock=bool(perm_row[2]),
                    add_products=bool(perm_row[3]),
                    view_notifications=bool(perm_row[4]),
                    create_client_list=bool(perm_row[5]),
                    view_orders=bool(perm_row[6]),
                    add_orders=bool(perm_row[7]),
                    change_order_state=bool(perm_row[8]),
                    create_bills=bool(perm_row[9]),
                    view_salaries=bool(perm_row[10]),
                    user_administration=bool(perm_row[11])
                )
                users.append(User(row[0], row[1], row[2], row[3], permissions))
        return users

    def get_user_by_username(self, username: str) -> typing.Optional[User]:
        self.c.execute('SELECT * FROM User WHERE Username = ?', (username,))
        row = self.c.fetchone()
        if row:
            self.c.execute('SELECT * FROM UserPermissions WHERE UserId = ?', (row[0],))
            perm_row = self.c.fetchone()
            if perm_row:
                permissions = UserPermissions(
                    view_stock=bool(perm_row[1]),
                    edit_stock=bool(perm_row[2]),
                    add_products=bool(perm_row[3]),
                    view_notifications=bool(perm_row[4]),
                    create_client_list=bool(perm_row[5]),
                    view_orders=bool(perm_row[6]),
                    add_orders=bool(perm_row[7]),
                    change_order_state=bool(perm_row[8]),
                    create_bills=bool(perm_row[9]),
                    view_salaries=bool(perm_row[10]),
                    user_administration=bool(perm_row[11])
                )
                return User(row[0], row[1], row[2], row[3], permissions)
        return None
    
    def update_user(self, user: User):
        self.c.execute('''
            UPDATE User SET Username = ?, Password = ?, Fullname = ? WHERE Id = ?
        ''', (user.username, user.password, user.full_name, user.id))
        self.c.execute('''
            UPDATE UserPermissions SET ViewStock = ?, EditStock = ?, AddProduct = ?, ViewNotifications = ?, CreateClientList = ?, ViewOrders = ?, AddOrders = ?, ChangeOrderState = ?, ViewBills = ?, CreateBills = ?, ViewSalaries = ?, UserAdministration = ? WHERE UserId = ?
        ''', (user.permissions.view_stock, user.permissions.edit_stock, user.permissions.add_products, user.permissions.view_notifications, user.permissions.create_client_list, user.permissions.view_orders, user.permissions.add_orders, user.permissions.change_order_state, user.permissions.view_bills, user.permissions.create_bills, user.permissions.view_salaries, user.permissions.user_administration, user.id))
        self.conn.commit()

    def insert_user(self, user: User):
        self.c.execute('''
            INSERT INTO User (Username, Password, Fullname) VALUES (?, ?, ?)
        ''', (user.username, user.password, user.full_name))
        user_id = self.c.lastrowid
        self.c.execute('''
            INSERT INTO UserPermissions (UserId, ViewStock, EditStock, AddProduct, ViewNotifications, CreateClientList, ViewOrders, AddOrders, ChangeOrderState, ViewBills, CreateBills, ViewSalaries, UserAdministration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, user.permissions.view_stock, user.permissions.edit_stock, user.permissions.add_products, user.permissions.view_notifications, user.permissions.create_client_list, user.permissions.view_orders, user.permissions.add_orders, user.permissions.change_order_state, user.permissions.view_bills, user.permissions.create_bills, user.permissions.view_salaries, user.permissions.user_administration))
        self.conn.commit()

    def get_all_companies(self) -> list[Company]:
        self.c.execute('SELECT * FROM Company')
        companies = [Company(row[0], row[1]) for row in self.c.fetchall()]
        return companies

    def update_company(self, company: Company):
        self.c.execute('''
            UPDATE Company SET Name = ? WHERE CompanyCode = ?
        ''', (company.name, company.company_code))
        self.conn.commit()

    def insert_company(self, company: Company):
        self.c.execute('''
            INSERT INTO Company (Name) VALUES (?)
        ''', (company.name,))
        self.conn.commit()

    def get_all_categories(self) -> list[Category]:
        self.c.execute('SELECT * FROM Category')
        categories = [Category(row[0], row[1]) for row in self.c.fetchall()]
        return categories

    def update_category(self, category: Category):
        self.c.execute('''
            UPDATE Category SET Name = ? WHERE CategoryCode = ?
        ''', (category.name, category.category_code))
        self.conn.commit()

    def insert_category(self, category: Category):
        self.c.execute('''
            INSERT INTO Category (Name) VALUES (?)
        ''', (category.name,))
        self.conn.commit()

    def get_all_products(self) -> list[Product]:
        self.c.execute('SELECT * FROM Product')
        products = [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in self.c.fetchall()]
        return products

    def update_product(self, product: Product):
        self.c.execute('''
            UPDATE Product SET Name = ?, PurchaseCost = ?, SellingPrice = ?, Quantity = ?, QuantityLimit = ?, CompanyCode = ?, CategoryCode = ? WHERE ProductCode = ?
        ''', (product.name, product.purchase_cost, product.selling_price, product.quantity, product.quantity_limit, product.company_code, product.category_code, product.product_code))
        self.conn.commit()

    def insert_product(self, product: Product):
        self.c.execute('''
            INSERT INTO Product (Name, PurchaseCost, SellingPrice, Quantity, QuantityLimit, CompanyCode, CategoryCode) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product.name, product.purchase_cost, product.selling_price, product.quantity, product.quantity_limit, product.company_code, product.category_code))
        self.conn.commit()

    def insert_drug_batch(self, batch: DrugBatch):
        self.c.execute('''
            INSERT INTO DrugBatch (BatchCode, ProductCode, Quantity, ExpirationDate) VALUES (?, ?, ?, ?)
        ''', (batch.batch_code, batch.product_code, batch.quantity, batch.expiration_date))
        self.conn.commit()

    def update_drug_batch(self, batch: DrugBatch):
        self.c.execute('''
            UPDATE DrugBatch SET ProductCode = ?, Quantity = ?, ExpirationDate = ? WHERE BatchCode = ?
        ''', (batch.product_code, batch.quantity, batch.expiration_date, batch.batch_code))
        self.conn.commit()