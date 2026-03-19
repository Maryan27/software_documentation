from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import InsuranceProduct

engine = create_engine("sqlite:///insurance.db")
Session = sessionmaker(bind=engine)
session = Session()

count = session.query(InsuranceProduct).count()
print(f"Number of records in the database: {count}")

products = session.query(InsuranceProduct).limit(5).all()
for p in products:
    print(p.client_name, p.policy_number, p.insurance_type, p.amount, p.start_date)