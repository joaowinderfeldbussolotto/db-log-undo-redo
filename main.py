import json
from db import DB
import re

def print_transactions(transactions):
    for transaction in transactions:
        print("Transaction: {}".format(transaction['transaction']))
        print("ID: {}".format(transaction['id']))
        print("Column: {}".format(transaction['col']))
        print("Old Value: {}".format(transaction['old']))
        print("New Value: {}".format(transaction['new']))
        print("----------------------")


def getMetadata(metadata_file):
    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
    return metadata['INITIAL']

def load_log(log_file):
    with open(log_file, 'r') as file:
        log_data = file.read().splitlines()
    return log_data

#Se não tem commmit, segue

def redo(log):
    commited = []
    transactions = []
    for line in reversed(log):
        if (re.match('^<commit .+>', line)):
            transaction = re.sub('<commit|>', '', line).strip()
            #print(transaction)
            commited.append(transaction)

        elif (re.match('^<.+,.+,.+,.+,.+>', line)):
            args = re.sub('<|>| ', '', line)
            [transaction, id, col, old, new] = args.split(',')

            # Check if the entry already exists in transactions
            exists = False
            exists = any(entry['transaction'] == transaction and entry['id'] == id and entry['col'] == col for entry in transactions)

            if transaction in commited and not exists:
                transactions.append({
                'transaction': transaction,
                'id': id,
                'col': col,
                'old': old,
               'new': new})

    return transactions[::-1]
    
def verify_incosistency(id, column, value):
    r = db.exec(f"SELECT {column} FROM db_log WHERE id = {id} and {column} = '{value}'")
    if r == []:
        return False
    return r[0][0]

def redo_database(redo_transactions):
    for t in redo_transactions:
        if not verify_incosistency(t['id'], t['col'], t['new']):
          db.update(t['id'], t['col'], t['new'])
        
if __name__ == '__main__':
    db = DB()
    metadata_file = 'metadado.json'
    log_file = 'entradaLog(1)'
    metadata = getMetadata(metadata_file)
    log = load_log(log_file)
    db.create('db_log', list(metadata.keys()))
    db.populate('db_log', metadata)
    t = redo(log)
    redo_database(t)
    # for key, value in metadata.items():  
    #     db.populate(key, value) 
        


  
    
