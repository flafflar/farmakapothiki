from database import Company, DatabaseManager, User, UserPermissions    
import pytest

@pytest.fixture
def db(tmp_path):
    open(tmp_path / "database.sqlite", "w").close()
    db = DatabaseManager(tmp_path / "database.sqlite")
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
    companies = [Company("S000121", "Drugs"), Company("S000122", "Food"), Company("S000123", "Clothes")]
    return companies



def test_get_all_companies(db, companies):
    # Insert companies into the database
    for company in companies:
        db.insert_company(company)

    # Retrieve all companies using the method to be tested
    all_companies = db.get_all_companies()

    # Verify that the number of companies retrieved matches the number inserted
    assert len(all_companies) == len(companies)

    # Verify that each company retrieved matches the inserted companies
    for company in companies:
        c = [c for c in all_companies if c.company_code == company.company_code]
        assert len(c) == 1
        assert c[0].name == company.name




def test_update_company(db, companies):
    for company in companies:
        db.insert_company(company) 

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