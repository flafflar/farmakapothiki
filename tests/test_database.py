import pytest
from database import Category, Company, DatabaseManager, Product, User, UserPermissions
import sqlite3

class SQLiteDB:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.path = path

@pytest.fixture
def sqlite_db(tmp_path):
    return SQLiteDB(tmp_path / "database.sqlite")

@pytest.fixture
def db(sqlite_db):
    db = DatabaseManager(sqlite_db.path)
    return db

@pytest.fixture
def users():
    permissions = UserPermissions(
        view_stock=True, edit_stock=True, add_products=True,
        view_notifications=True, create_client_list=True,
        view_orders=True, add_orders=True, change_order_state=True,
        view_bills=True, create_bills=True, view_salaries=True,
        user_administration=True
    )
    return [
        User(0, "jdoe", "pass1", "John Doe", permissions),
        User(0, "bwayne", "pass2", "Bruce Wayne", permissions),
        User(0, "pparker", "pass3", "Peter Parker", permissions)
    ]

def insert_users(sqlite_db: SQLiteDB, users: list[User]):
    for user in users:
        sqlite_db.cur.execute("INSERT INTO User(Username, Password, FullName) VALUES (?, ?, ?)",
                               (user.username, user.password, user.full_name))
        user.id = sqlite_db.cur.lastrowid

        sqlite_db.cur.execute('''INSERT INTO UserPermissions(UserId, ViewStock, EditStock, AddProduct, ViewNotifications, CreateClientList, ViewOrders, AddOrders, ChangeOrderState, ViewBills, CreateBills, ViewSalaries, UserAdministration)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (user.id, user.permissions.view_stock, user.permissions.edit_stock,
                               user.permissions.add_products, user.permissions.view_notifications,
                               user.permissions.create_client_list, user.permissions.view_orders,
                               user.permissions.add_orders, user.permissions.change_order_state,
                               user.permissions.view_bills, user.permissions.create_bills,
                               user.permissions.view_salaries, user.permissions.user_administration))
        sqlite_db.con.commit()

def test_get_all_users(sqlite_db: SQLiteDB, db: DatabaseManager, users: list[User]):
    insert_users(sqlite_db, users)

    all_users = db.get_all_users()

    assert len(all_users) == len(users)

    for user in users:
        u = [u for u in all_users if u.id == user.id]
        assert len(u) == 1
        assert u[0].username == user.username
        assert u[0].password == user.password
        assert u[0].full_name == user.full_name
        assert u[0].permissions.view_stock == user.permissions.view_stock
        assert u[0].permissions.edit_stock == user.permissions.edit_stock
        assert u[0].permissions.add_products == user.permissions.add_products
        assert u[0].permissions.view_notifications == user.permissions.view_notifications
        assert u[0].permissions.create_client_list == user.permissions.create_client_list
        assert u[0].permissions.view_orders == user.permissions.view_orders
        assert u[0].permissions.add_orders == user.permissions.add_orders
        assert u[0].permissions.change_order_state == user.permissions.change_order_state
        assert u[0].permissions.view_bills == user.permissions.view_bills
        assert u[0].permissions.create_bills == user.permissions.create_bills
        assert u[0].permissions.view_salaries == user.permissions.view_salaries
        assert u[0].permissions.user_administration == user.permissions.user_administration


def test_update_user(sqlite_db: SQLiteDB, db: DatabaseManager, users: list[User]):
    insert_users(sqlite_db, users)

    for user in users:
        user.username += "Updated"
        user.password += "Updated"
        user.full_name += "Updated"
        user.permissions.view_stock = not user.permissions.view_stock
        user.permissions.edit_stock = not user.permissions.edit_stock
        user.permissions.add_products = not user.permissions.add_products
        user.permissions.view_notifications = not user.permissions.view_notifications
        user.permissions.create_client_list = not user.permissions.create_client_list
        user.permissions.view_orders = not user.permissions.view_orders
        user.permissions.add_orders = not user.permissions.add_orders
        user.permissions.change_order_state = not user.permissions.change_order_state
        user.permissions.view_bills = not user.permissions.view_bills
        user.permissions.create_bills = not user.permissions.create_bills
        user.permissions.view_salaries = not user.permissions.view_salaries
        user.permissions.user_administration = not user.permissions.user_administration

        db.update_user(user)

    all_users = db.get_all_users()

    assert len(all_users) == len(users)

    for user in users:
        u = [u for u in all_users if u.id == user.id]
        assert len(u) == 1
        assert u[0].username == user.username
        assert u[0].password == user.password
        assert u[0].full_name == user.full_name
        assert u[0].permissions.view_stock == user.permissions.view_stock
        assert u[0].permissions.edit_stock == user.permissions.edit_stock
        assert u[0].permissions.add_products == user.permissions.add_products
        assert u[0].permissions.view_notifications == user.permissions.view_notifications
        assert u[0].permissions.create_client_list == user.permissions.create_client_list
        assert u[0].permissions.view_orders == user.permissions.view_orders
        assert u[0].permissions.add_orders == user.permissions.add_orders
        assert u[0].permissions.change_order_state == user.permissions.change_order_state
        assert u[0].permissions.view_bills == user.permissions.view_bills
        assert u[0].permissions.create_bills == user.permissions.create_bills
        assert u[0].permissions.view_salaries == user.permissions.view_salaries
        assert u[0].permissions.user_administration == user.permissions.user_administration


def test_insert_user(sqlite_db: SQLiteDB, db: DatabaseManager, users: list[User]):
    for user in users:
        db.insert_user(user)

        sqlite_db.cur.execute("SELECT * FROM User WHERE Username = ?", (user.username,))
        assert len(sqlite_db.cur.fetchall()) == 1


@pytest.fixture
def companies():
    return [
        Company("", "Drugs"),
        Company("", "Food"),
        Company("", "Clothes")
    ]

def insert_companies(sqlite_db: SQLiteDB, companies: list[Company]):
    for company in companies:
        sqlite_db.cur.execute("INSERT INTO Company(Name) VALUES (?)", (company.name,))
        company.company_code = f"C{sqlite_db.cur.lastrowid:06}"
        sqlite_db.con.commit()

def test_get_all_companies(sqlite_db: SQLiteDB, db: DatabaseManager, companies: list[Company]):
    for company in companies:
        sqlite_db.cur.execute("INSERT INTO Company(Name) VALUES (:name)", {"name": company.name})

    companies = db.get_all_companies()

    for company in companies:
        c = [c for c in companies if c.name == company.name]
        assert len(c) == 1

def test_update_company(sqlite_db: SQLiteDB, db: DatabaseManager, companies: list[Company]):
    insert_companies(sqlite_db, companies)

    for company in companies:
        company.name += " Updated"
        db.update_company(company)

    for company in companies:
        sqlite_db.cur.execute("SELECT Name FROM Company WHERE CompanyCode = ?", (company.company_code_int,))
        assert sqlite_db.cur.fetchone()[0] == company.name

def test_insert_company(sqlite_db: SQLiteDB, db: DatabaseManager, companies: list[Company]):
    for company in companies:
        db.insert_company(company)

        sqlite_db.cur.execute("SELECT * FROM Company WHERE Name = ?", (company.name,))
        assert len(sqlite_db.cur.fetchall()) == 1

@pytest.fixture
def sample_categories():
    return [
        Category("", "Κατηγορία 1"),
        Category("", "Κατηγορία 2"),
        Category("", "Κατηγορία 3"),
    ]

def insert_categories(sqlite_db: SQLiteDB, categories: list[Category]):
    for category in categories:
        sqlite_db.cur.execute("INSERT INTO Category(Name) VALUES (?)", (category.name,))
        category.category_code = f"C{sqlite_db.cur.lastrowid:06}"
        sqlite_db.con.commit()

def test_get_all_categories(sqlite_db: SQLiteDB, db: DatabaseManager, sample_categories: list[Category]):
    for category in sample_categories:
        sqlite_db.cur.execute("INSERT INTO Category(Name) VALUES (:name)", {"name": category.name})

    categories = db.get_all_categories()

    for category in categories:
        c = [c for c in sample_categories if c.name == category.name]
        assert len(c) == 1

def test_update_category(sqlite_db: SQLiteDB, db: DatabaseManager, sample_categories: list[Category]):
    insert_categories(sqlite_db, sample_categories)

    for category in sample_categories:
        category.name += " Updated"
        db.update_category(category)

    for category in sample_categories:
        sqlite_db.cur.execute("SELECT Name FROM Category WHERE CategoryCode = ?", (category.category_code_int,))
        assert sqlite_db.cur.fetchone()[0] == category.name

def test_insert_category(sqlite_db: SQLiteDB, db: DatabaseManager, sample_categories: list[Category]):
    for category in sample_categories:
        db.insert_category(category)

        sqlite_db.cur.execute("SELECT * FROM Category WHERE Name = ?", (category.name,))
        assert len(sqlite_db.cur.fetchall()) == 1




