class DataWriter:
    def __init__(self, strategy):
        self.strategy = strategy

    def write_data(self, data):
        self.strategy.write(data)