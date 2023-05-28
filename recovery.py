import re
from db import DB

db = DB()

def get_commited(log):
    commited = []
    for line in reversed(log):
        if (re.match('^<commit .+>', line)):
            transaction = re.sub('<commit|>', '', line).strip()
            commited.append(transaction)
    return commited

def get_uncommited(log, commited):
    uncommited = set()
    for line in log:
        if not line.startswith('<start') and not line.startswith('<commit'):
            t = re.sub('<|>| ', '', line).split(',')[0]
            if t not in commited:
                uncommited.add(t)

    return list(uncommited)

def undo(log, uncommited):
    transactions = []
    for line in reversed(log):
        if (re.match('^<.+,.+,.+,.+,.+>', line)):
            args = re.sub('<|>| ', '', line)
            [transaction, id, col, old, new] = args.split(',')

            # Check if the entry already exists in transactions
            exists = False
            # exists = any(entry['transaction'] == transaction and entry['id'] == id and entry['col'] == col for entry in transactions)

            if transaction in uncommited and not exists:
                transactions.append({
                'transaction': transaction,
                'id': id,
                'col': col,
                'old': old,
               'new': new})

    return transactions

def redo(log,commited):
    transactions = []
    for line in log:
        if (re.match('^<.+,.+,.+,.+,.+>', line)):
            args = re.sub('<|>| ', '', line)
            [transaction, id, col, old, new] = args.split(',')

            # Check if the entry already exists in transactions
            exists = False
            # exists = any(entry['transaction'] == transaction and entry['id'] == id and entry['col'] == col for entry in transactions)

            if transaction in commited and not exists:
                transactions.append({
                'transaction': transaction,
                'id': id,
                'col': col,
                'old': old,
               'new': new})

    return transactions
    
def verify_incosistency(id, column, value):
    r = db.exec(f"SELECT {column} FROM db_log WHERE id = {id} and {column} = '{value}'")
    if r == []:
        return False
    return r[0][0]

def redo_db(transactions):
    for t in transactions:
        if not verify_incosistency(t['id'], t['col'], t['new']):
            db.update(t['id'], t['col'], t['new'])

def undo_db(transactions):
    for t in transactions:
        if not verify_incosistency(t['id'], t['col'], t['old']):
            db.update(t['id'], t['col'], t['old'])