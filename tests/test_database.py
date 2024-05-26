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
    users = [
        User(10, "jdoe", "pass1", "John Doe", permissions),
        User(11, "bwayne", "pass2", "Bruce Wayne", permissions),
        User(12, "pparker", "pass3", "Peter Parker", permissions)
    ]
    return users

def test_get_all_users(db, users):
    # Insert the initial users into the database
    for user in users:
        db.insert_user(user)

    # Fetch all users from the database
    all_users = db.get_all_users()

    # Verify the number of users retrieved
    assert len(all_users) == len(users)

    # Verify each user's details and permissions
    for user in users:
        u = [u for u in all_users if u.id == user.id]
        assert len(u) == 1
        assert u[0].username == user.username
        assert u[0].full_name == user.full_name
        assert u[0].password == user.password

        # Check permissions
        user_permissions = u[0].permissions
        assert user_permissions.view_stock == user.permissions.view_stock
        assert user_permissions.edit_stock == user.permissions.edit_stock
        assert user_permissions.add_products == user.permissions.add_products
        assert user_permissions.view_notifications == user.permissions.view_notifications
        assert user_permissions.create_client_list == user.permissions.create_client_list
        assert user_permissions.view_orders == user.permissions.view_orders
        assert user_permissions.add_orders == user.permissions.add_orders
        assert user_permissions.change_order_state == user.permissions.change_order_state
        assert user_permissions.view_bills == user.permissions.view_bills
        assert user_permissions.create_bills == user.permissions.create_bills
        assert user_permissions.view_salaries == user.permissions.view_salaries
        assert user_permissions.user_administration == user.permissions.user_administration


def test_insert_user(db, users):
    for user in users:
        db.insert_user(user)

    all_users = db.get_all_users()  # Retrieve all users from the database

    assert len(all_users) == len(users)

    for user in users:
        u = [u for u in all_users if u.username == user.username]
        assert len(u) == 1
        assert u[0].username == user.username
        assert u[0].full_name == user.full_name
        assert u[0].password == user.password

        # Check permissions
        user_permissions = u[0].permissions
        assert user_permissions.view_stock == user.permissions.view_stock
        assert user_permissions.edit_stock == user.permissions.edit_stock
        assert user_permissions.add_products == user.permissions.add_products
        assert user_permissions.view_notifications == user.permissions.view_notifications
        assert user_permissions.create_client_list == user.permissions.create_client_list
        assert user_permissions.view_orders == user.permissions.view_orders
        assert user_permissions.add_orders == user.permissions.add_orders
        assert user_permissions.change_order_state == user.permissions.change_order_state
        assert user_permissions.view_bills == user.permissions.view_bills
        assert user_permissions.create_bills == user.permissions.create_bills
        assert user_permissions.view_salaries == user.permissions.view_salaries
        assert user_permissions.user_administration == user.permissions.user_administration


def test_update_user(db, users):
    # Insert the initial users into the database
    for user in users:
        db.insert_user(user)

    # Update each user's details
    for user in users:
        user.username += "_updated"
        user.password += "_updated"
        user.full_name += " Updated"
        # Update permissions for testing
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

    # Retrieve all users from the database
    all_users = db.get_all_users()

    assert len(all_users) == len(users)

    for user in users:
        u = [u for u in all_users if u.id == user.id]
        assert len(u) == 1
        assert u[0].username == user.username
        assert u[0].full_name == user.full_name
        assert u[0].password == user.password

        # Check updated permissions
        user_permissions = u[0].permissions
        assert user_permissions.view_stock == user.permissions.view_stock
        assert user_permissions.edit_stock == user.permissions.edit_stock
        assert user_permissions.add_products == user.permissions.add_products
        assert user_permissions.view_notifications == user.permissions.view_notifications
        assert user_permissions.create_client_list == user.permissions.create_client_list
        assert user_permissions.view_orders == user.permissions.view_orders
        assert user_permissions.add_orders == user.permissions.add_orders
        assert user_permissions.change_order_state == user.permissions.change_order_state
        assert user_permissions.view_bills == user.permissions.view_bills
        assert user_permissions.create_bills == user.permissions.create_bills
        assert user_permissions.view_salaries == user.permissions.view_salaries
        assert user_permissions.user_administration == user.permissions.user_administration

def test_get_user_by_username(db, users):
    # Insert the initial users into the database
    for user in users:
        db.insert_user(user)

    # Fetch each user by username and verify the retrieved data
    for user in users:
        fetched_user = db.get_user_by_username(user.username)
        assert fetched_user is not None
        assert fetched_user.id == user.id
        assert fetched_user.username == user.username
        assert fetched_user.full_name == user.full_name
        assert fetched_user.password == user.password

        # Check permissions
        user_permissions = fetched_user.permissions
        assert user_permissions.view_stock == user.permissions.view_stock
        assert user_permissions.edit_stock == user.permissions.edit_stock
        assert user_permissions.add_products == user.permissions.add_products
        assert user_permissions.view_notifications == user.permissions.view_notifications
        assert user_permissions.create_client_list == user.permissions.create_client_list
        assert user_permissions.view_orders == user.permissions.view_orders
        assert user_permissions.add_orders == user.permissions.add_orders
        assert user_permissions.change_order_state == user.permissions.change_order_state
        assert user_permissions.view_bills == user.permissions.view_bills
        assert user_permissions.create_bills == user.permissions.create_bills
        assert user_permissions.view_salaries == user.permissions.view_salaries
        assert user_permissions.user_administration == user.permissions.user_administration


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
        company.company_code = f"S{sqlite_db.cur.lastrowid:06}"
        sqlite_db.con.commit()

def test_get_all_companies(sqlite_db, db, companies):
    # Insert companies into the database
    insert_companies(sqlite_db, companies)

    # Retrieve all companies using the method to be tested
    all_companies = db.get_all_companies()

    # Verify that the number of companies retrieved matches the number inserted
    assert len(all_companies) == len(companies)

    # Verify that each company retrieved matches the inserted companies
    for company in companies:
        c = [c for c in all_companies if c.company_code == company.company_code]
        assert len(c) == 1
        assert c[0].name == company.name

def test_update_company(sqlite_db, db, companies):
    insert_companies(sqlite_db, companies)

    for company in companies:
        company.name = company.name + "a"
        db.update_company(company)

    all_companies = db.get_all_companies()

    assert len(all_companies) == len(companies)

    for company in companies:
        c = [c for c in all_companies if c.company_code == company.company_code]
        assert len(c) == 1
        assert c[0].name == company.name

#TODO Fix the inserts since the main code takes random id values and the test code takes fixed id values

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