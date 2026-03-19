import csv

class CSVReader:
    def __init__(self, filepath, max_rows=None):
        self.filepath = filepath
        self.max_rows = max_rows  

    def read(self):
        data = []
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if self.max_rows and i >= self.max_rows:
                    break
                data.append(row)
        return data