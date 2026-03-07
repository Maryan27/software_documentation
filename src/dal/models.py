from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InsuranceProduct(Base):
    __tablename__ = "insurance_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String)
    client_email = Column(String)
    policy_number = Column(String)
    insurance_type = Column(String)
    amount = Column(Float)
    company_name = Column(String)
    start_date = Column(Date)