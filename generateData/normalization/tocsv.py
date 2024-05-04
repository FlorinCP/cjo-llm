import pandas as pd


def json_to_csv(json_file, csv_file):
    df = pd.read_json(json_file)
    print(df.head())
    df.to_csv(csv_file, index=False)


json_file_path = './working_data_labeled.json'
csv_file_path = './dataset.tsv'

json_to_csv(json_file_path, csv_file_path)
