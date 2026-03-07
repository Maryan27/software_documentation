from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import Base
from src.dal.data_access import CSVAndDBAccess
from src.bll.business_logic import InsuranceManager

def main():
    engine = create_engine("sqlite:///insurance.db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    data_access = CSVAndDBAccess(session)

    manager = InsuranceManager(data_access)

    manager.import_csv_to_db("insurance_data.csv")

if __name__ == "__main__":
    main()