from database import Company, DatabaseManager
import pytest

@pytest.fixture
def db(tmp_path):
    open(tmp_path / "database.sqlite", "w").close()
    db = DatabaseManager(tmp_path / "database.sqlite")
    return db

@pytest.fixture
def companies():
    companies = [Company("S0121", "Drugs"), Company("S0122", "Food"), Company("S0123", "Clothes")]
    return companies
 
def test_insert_company(db, companies):
    for company in companies:
        db.insert_company(company)
    
    all_companies = db.get_all_companies()  

    assert len(all_companies) ==  len(companies)

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
