import json

def print_table(headers, table):
    column_widths = [max(len(str(item)) for item in column) for column in zip(*table)]

    # Print the headers
    header_row = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))

    # Print the rows
    for row in table :
        formatted_row = " | ".join(f"{item:<{width}}" for item, width in zip(row, column_widths))
        print(formatted_row)

def print_transactions(transactions):
    for transaction in transactions:
        print("Transaction: {}".format(transaction['transaction']))
        print("ID: {}".format(transaction['id']))
        print("Column: {}".format(transaction['col']))
        print("Old Value: {}".format(transaction['old']))
        print("New Value: {}".format(transaction['new']))
        print("----------------------")

def get_metadata(metadata_file):
    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
    return metadata['INITIAL']

def load_log(log_file):
    with open(log_file, 'r') as file:
        log_data = file.read().splitlines()
    return log_data

