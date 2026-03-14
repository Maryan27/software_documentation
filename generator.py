import csv
import random
from faker import Faker

def generate_csv(filename="insurance_data.csv", num_rows=1000):
    fake = Faker()

    insurance_types = ['Life', 'Health', 'Vehicle', 'Property', 'Travel']
    
    print(f"Starting generation of {num_rows} rows into file {filename}...")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            'client_name',     
            'client_email',    
            'policy_number',    
            'insurance_type',   
            'amount',           
            'company_name',     
            'start_date'        
        ])

        for _ in range(num_rows):
            writer.writerow([
                fake.name(),
                fake.email(),
                fake.bothify(text='POL-######-??'),
                random.choice(insurance_types),
                round(random.uniform(1000, 100000), 2),
                fake.company() + " Insurance",
                fake.date_this_decade()
            ])

    print(f"Done! File '{filename}' has been created.")

if __name__ == "__main__":
    generate_csv("insurance_data.csv", 1005) 