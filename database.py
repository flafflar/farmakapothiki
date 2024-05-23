import datetime
import sqlite3
import typing
class Company:
    """
    Represents a company with a unique company code and name.

    Attributes:
        company_code (str): The unique identifier for the company.
        name (str): The name of the company.
    """
    def __init__(self, company_code: str, name: str):
        """
        Initializes a new instance of the Company class.

        Args:
            company_code (str): The unique identifier for the company.
            name (str): The name of the company.
        """
        self.company_code = company_code
        self.name = name

class Category:
    """
    Represents a category with a unique category code and name.

    Attributes:
        category_code (str): The unique identifier for the category.
        name (str): The name of the category.
    """
    def __init__(self, category_code: str, name: str):
        """
        Initializes a new instance of the Category class.

        Args:
            category_code (str): The unique identifier for the category.
            name (str): The name of the category.
        """
        self.category_code = category_code
        self.name = name
class Product:
    """
    Represents a product with a unique product code, name, purchase cost, selling price, quantity, quantity limit, company, and category.

    Attributes:
        product_code (str): The unique identifier for the product.
        name (str): The name of the product.
        purchase_cost (float): The cost of purchasing the product.
        selling_price (float): The price at which the product is sold.
        quantity (int): The quantity of the product in stock.
        quantity_limit (int): The minimum quantity of the product that should be in stock.
        company (Company): The company that produces the product.
        category (Category): The category to which the product belongs.
    """
    def __init__(self, product_code: str, name: str, purchase_cost: float, selling_price: float, quantity: int, quantity_limit: int, company: Company, category: Category):
        """
        Initializes a new instance of the Product class.

        Args:
            product_code (str): The unique identifier for the product.
            name (str): The name of the product.
            purchase_cost (float): The cost of purchasing the product.
            selling_price (float): The price at which the product is sold.
            quantity (int): The quantity of the product in stock.
            quantity_limit (int): The minimum quantity of the product that should be in stock.
            company (Company): The company that produces the product.
            category (Category): The category to which the product belongs.
        """
        self.product_code = product_code
        self.name = name
        self.purchase_cost = purchase_cost
        self.selling_price = selling_price
        self.quantity = quantity
        self.quantity_limit = quantity_limit
        self.company = company
        self.category = category

class DrugBatch:
    """
    Represents a batch of drugs with a unique batch code, quantity, and expiration date.

    Attributes:
        batch_code (str): The unique identifier for the drug batch.
        quantity (int): The quantity of drugs in the batch.
        expiration_date (datetime): The date when the drugs in the batch expire.
    """
    def __init__(self, batch_code: str, quantity: int, expiration_date: datetime):
        """
        Initializes a new instance of the DrugBatch class.

        Args:
            batch_code (str): The unique identifier for the drug batch.
            quantity (int): The quantity of drugs in the batch.
            expiration_date (datetime): The date when the drugs in the batch expire.
        """
        self.batch_code = batch_code
        self.quantity = quantity
        self.expiration_date = expiration_date
    
class Drug(Product):
    """
    Represents a drug, which is a type of product, with a unique product code, name, purchase cost, selling price, quantity, quantity limit, quality, and batches.

    Attributes:
        product_code (str): The unique identifier for the drug.
        name (str): The name of the drug.
        purchase_cost (float): The cost of purchasing the drug.
        selling_price (float): The price at which the drug is sold.
        quantity (int): The quantity of the drug in stock.
        quantity_limit (int): The minimum quantity of the drug that should be in stock.
        quality (bool): The quality of the drug. True if the drug is of high quality, False otherwise.
        batches (list): A list of DrugBatch objects representing the batches of the drug.
    """
    def __init__(self, product_code: str, name: str, purchase_cost: float, selling_price: float, quantity, quantity_limit, quality: bool, batches: list):
        """
        Initializes a new instance of the Drug class.

        Args:
            product_code (str): The unique identifier for the drug.
            name (str): The name of the drug.
            purchase_cost (float): The cost of purchasing the drug.
            selling_price (float): The price at which the drug is sold.
            quantity (int): The quantity of the drug in stock.
            quantity_limit (int): The minimum quantity of the drug that should be in stock.
            quality (bool): The quality of the drug. True if the drug is of high quality, False otherwise.
            batches (list): A list of DrugBatch objects representing the batches of the drug.
        """
        super().__init__(product_code, name, purchase_cost, selling_price, quantity, quantity_limit)
        self.quality = quality
        self.batches = batches
 
class UserPermissions:
    """
    Represents the permissions a user has in the system.

    Attributes:
        view_stock (bool): Permission to view stock.
        edit_stock (bool): Permission to edit stock.
        add_products (bool): Permission to add products.
        view_notifications (bool): Permission to view notifications.
        create_client_list (bool): Permission to create client list.
        view_orders (bool): Permission to view orders.
        add_orders (bool): Permission to add orders.
        change_order_state (bool): Permission to change the state of orders.
        create_bills (bool): Permission to create bills.
        view_salaries (bool): Permission to view salaries.
        user_administration (bool): Permission for user administration.
    """
    def __init__(self):
        """
        Initializes a new instance of the UserPermissions class with all permissions set to False.
        """
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
    """
    Represents a user in the system with a unique ID, username, password, full name, and permissions.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The password of the user.
        full_name (str): The full name of the user.
        permissions (UserPermissions): The permissions the user has in the system.
    """
    def __init__(self, id: int, username: str, password: str, full_name: str, permissions: UserPermissions):
        """
        Initializes a new instance of the User class.

        Args:
            id (int): The unique identifier for the user.
            username (str): The username of the user.
            password (str): The password of the user.
            full_name (str): The full name of the user.
            permissions (UserPermissions): The permissions the user has in the system.
        """
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.permissions = permissions

class DatabaseManager:
    """
    Manages interactions with the SQLite3 database.

    Attributes:
        conn (sqlite3.Connection): The connection to the SQLite3 database.
        c (sqlite3.Cursor): The cursor for executing SQL statements.
    """
    def __init__(self):
        """
        Initializes a new instance of the DatabaseManager class, establishing a connection to the SQLite3 database and creating a cursor for executing SQL statements.
        """
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """
        Creates the tables in the SQLite3 database if they do not already exist.
        """
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
        """
        Retrieves all users from the User table in the database.

        Each user's permissions are also retrieved from the UserPermissions table.

        Returns:
            list[User]: A list of User objects representing all users in the database. Each User object includes the user's permissions.
        """
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
        """
        Retrieves a user from the User table in the database by their username.

        The user's permissions are also retrieved from the UserPermissions table.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: A User object representing the user with the given username, if found. The User object includes the user's permissions.
            None: If no user with the given username is found.
        """
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
        """
        Updates a user's details and permissions in the User and UserPermissions tables in the database.

        Args:
            user (User): The User object containing the updated details and permissions of the user.

        The method updates the user's username, password, and full name in the User table and the user's permissions in the UserPermissions table.
        """
        self.c.execute('''
            UPDATE User SET Username = ?, Password = ?, Fullname = ? WHERE Id = ?
        ''', (user.username, user.password, user.full_name, user.id))
        self.c.execute('''
            UPDATE UserPermissions SET ViewStock = ?, EditStock = ?, AddProduct = ?, ViewNotifications = ?, CreateClientList = ?, ViewOrders = ?, AddOrders = ?, ChangeOrderState = ?, ViewBills = ?, CreateBills = ?, ViewSalaries = ?, UserAdministration = ? WHERE UserId = ?
        ''', (user.permissions.view_stock, user.permissions.edit_stock, user.permissions.add_products, user.permissions.view_notifications, user.permissions.create_client_list, user.permissions.view_orders, user.permissions.add_orders, user.permissions.change_order_state, user.permissions.view_bills, user.permissions.create_bills, user.permissions.view_salaries, user.permissions.user_administration, user.id))
        self.conn.commit()

    def insert_user(self, user: User):
        """
        Inserts a new user into the User and UserPermissions tables in the database.

        Args:
            user (User): The User object containing the details and permissions of the user to insert.

        The method inserts the user's username, password, and full name into the User table and the user's permissions into the UserPermissions table.
        """
        self.c.execute('''
            INSERT INTO User (Username, Password, Fullname) VALUES (?, ?, ?)
        ''', (user.username, user.password, user.full_name))
        user_id = self.c.lastrowid
        self.c.execute('''
            INSERT INTO UserPermissions (UserId, ViewStock, EditStock, AddProduct, ViewNotifications, CreateClientList, ViewOrders, AddOrders, ChangeOrderState, ViewBills, CreateBills, ViewSalaries, UserAdministration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, user.permissions.view_stock, user.permissions.edit_stock, user.permissions.add_products, user.permissions.view_notifications, user.permissions.create_client_list, user.permissions.view_orders, user.permissions.add_orders, user.permissions.change_order_state, user.permissions.view_bills, user.permissions.create_bills, user.permissions.view_salaries, user.permissions.user_administration))
        self.conn.commit()

    def get_all_companies(self) -> list[Company]:
        """
        Retrieves all companies from the Company table in the database.

        Returns:
            list[Company]: A list of Company objects representing all companies in the database.
        """
        self.c.execute('SELECT * FROM Company')
        companies = [Company(row[0], row[1]) for row in self.c.fetchall()]
        return companies

    def update_company(self, company: Company):
        """
        Updates a company's name in the Company table in the database.

        Args:
            company (Company): The Company object containing the updated name of the company.
        """
        self.c.execute('''
            UPDATE Company SET Name = ? WHERE CompanyCode = ?
        ''', (company.name, company.company_code))
        self.conn.commit()

    def insert_company(self, company: Company):
        """
        Inserts a new company into the Company table in the database.

        Args:
            company (Company): The Company object containing the name of the company to insert.
        """
        self.c.execute('''
            INSERT INTO Company (Name) VALUES (?)
        ''', (company.name,))
        self.conn.commit()

    def get_all_categories(self) -> list[Category]:
        """
        Retrieves all categories from the Category table in the database.

        Returns:
            list[Category]: A list of Category objects representing all categories in the database.
        """
        self.c.execute('SELECT * FROM Category')
        categories = [Category(row[0], row[1]) for row in self.c.fetchall()]
        return categories

    def update_category(self, category: Category):
        """
        Updates a category's name in the Category table in the database.

        Args:
            category (Category): The Category object containing the updated name of the category.
        """
        self.c.execute('''
            UPDATE Category SET Name = ? WHERE CategoryCode = ?
        ''', (category.name, category.category_code))
        self.conn.commit()

    def insert_category(self, category: Category):
        """
        Inserts a new category into the Category table in the database.
        
        Args:
            category (Category): The Category object containing the name of the category to insert.
        """
        self.c.execute('''
            INSERT INTO Category (Name) VALUES (?)
        ''', (category.name,))
        self.conn.commit()

    def get_all_products(self) -> list[Product]:
        """
        Retrieves all products from the Product table in the database.
        
        Returns:
            list[Product]: A list of Product objects representing all products in the database.
        """
        self.c.execute('SELECT * FROM Product')
        products = [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in self.c.fetchall()]
        return products

    def update_product(self, product: Product):
        """
        Updates a product's details in the Product table in the database.

        Args:
            product (Product): The Product object containing the updated details of the product.
        """
        self.c.execute('''
            UPDATE Product SET Name = ?, PurchaseCost = ?, SellingPrice = ?, Quantity = ?, QuantityLimit = ?, CompanyCode = ?, CategoryCode = ? WHERE ProductCode = ?
        ''', (product.name, product.purchase_cost, product.selling_price, product.quantity, product.quantity_limit, product.company_code, product.category_code, product.product_code))
        self.conn.commit()

    def insert_product(self, product: Product):
        """
        Inserts a new product into the Product table in the database.
        
        Args:
            product (Product): The Product object containing the details of the product to insert.
        """
        self.c.execute('''
            INSERT INTO Product (Name, PurchaseCost, SellingPrice, Quantity, QuantityLimit, CompanyCode, CategoryCode) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product.name, product.purchase_cost, product.selling_price, product.quantity, product.quantity_limit, product.company_code, product.category_code))
        self.conn.commit()

    def insert_drug_batch(self, batch: DrugBatch):
        """
        Inserts a new drug batch into the DrugBatch table in the database.
        
        Args:
            batch (DrugBatch): The DrugBatch object containing the details of the drug batch to insert.
        """
        self.c.execute('''
            INSERT INTO DrugBatch (BatchCode, ProductCode, Quantity, ExpirationDate) VALUES (?, ?, ?, ?)
        ''', (batch.batch_code, batch.product_code, batch.quantity, batch.expiration_date))
        self.conn.commit()

    def update_drug_batch(self, batch: DrugBatch):
        """
        Updates a drug batch's details in the DrugBatch table in the database.
        
        Args:
            batch (DrugBatch): The DrugBatch object containing the updated details of the drug batch.
        """
        self.c.execute('''
            UPDATE DrugBatch SET ProductCode = ?, Quantity = ?, ExpirationDate = ? WHERE BatchCode = ?
        ''', (batch.product_code, batch.quantity, batch.expiration_date, batch.batch_code))
        self.conn.commit()