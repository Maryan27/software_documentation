import csv
from datetime import datetime
from src.dal.models import InsuranceProduct  

class IInsuranceDataAccess:
    def save_all(self, items):
        raise NotImplementedError
    
    def load_from_csv(self, filepath):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

class CSVAndDBAccess(IInsuranceDataAccess):
    def __init__(self, session):
        self.session = session

    def load_from_csv(self, filepath):
        products = []
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_number, row in enumerate(reader, start=1):
                if not row['client_name'] or not row['client_email'] or not row['policy_number'] or not row['insurance_type'] or not row['amount']:
                    print(f"Row {row_number} skipped: missing required fields")
                    continue  

                try:
                    start_date = datetime.strptime(row['start_date'], "%Y-%m-%d").date()
                except:
                    start_date = None  

                try:
                    amount = float(row['amount'])
                except ValueError:
                    print(f"Row {row_number} skipped: invalid amount '{row['amount']}'")
                    continue

                product = InsuranceProduct(
                    client_name=row['client_name'],
                    client_email=row['client_email'],
                    policy_number=row['policy_number'],
                    insurance_type=row['insurance_type'],
                    amount=amount,
                    company_name=row.get('company_name', ''),  
                    start_date=start_date
                )
                products.append(product)
        return products

    def save_all(self, items):
        if not items:
            print("No valid products to save.")
            return
        try:
            self.session.add_all(items)
            self.session.commit()
            print(f"{len(items)} products saved to the database")
        except Exception as e:
            self.session.rollback()
            print(f"Error saving products: {e}")

    def get_all(self):
        return self.session.query(InsuranceProduct).all()