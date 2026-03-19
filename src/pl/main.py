from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import Base
from src.dal.data_access import CSVAndDBAccess
from src.bll.business_logic import InsuranceManager

def main():
    print("=== Starting CSV import to database ===")

    engine = create_engine("sqlite:///insurance.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    data_access = CSVAndDBAccess(session)
    manager = InsuranceManager(data_access)

    print("Importing data from CSV...")
    manager.import_csv_to_db("insurance_data.csv")
    print("=== CSV import completed ===")

if __name__ == "__main__":
    main()