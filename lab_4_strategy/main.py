import json
from csv_reader import CSVReader
from output_strategy import ConsoleOutput, KafkaOutput, RedisOutput
from data_writer import DataWriter

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

strategy_name = config.get("output_strategy", "console").lower()
if strategy_name == "console":
    strategy = ConsoleOutput()
elif strategy_name == "kafka":
    strategy = KafkaOutput()
elif strategy_name == "redis":
    strategy = RedisOutput()
else:
    strategy = ConsoleOutput()

writer = DataWriter(strategy)

data = CSVReader(config.get("csv_file_path", "Dallas_Police_Incidents_s.csv"), max_rows=1000).read()

writer.write_data(data)