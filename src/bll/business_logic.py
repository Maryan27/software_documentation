class InsuranceManager:
    def __init__(self, data_access):
        self.data_access = data_access

    def import_csv_to_db(self, filepath):
        products = self.data_access.load_from_csv(filepath)
        print(f"Read {len(products)} records from CSV")
        self.data_access.save_all(products)
        print("Data has been saved to the database")

    def get_all_products(self):
        return self.data_access.get_all()