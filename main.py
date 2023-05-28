# -*- coding: utf-8 -*-
from db import DB
from recovery import get_commited, get_uncommited, redo, undo
from utils import print_table, load_log, get_metadata

if __name__ == '__main__':

    db = DB()
    METADATA_FILE = 'files/metadado.json'
    LOG_FILE = 'files/entradaLog(1)'
    metadata = get_metadata(METADATA_FILE)
    log = load_log(LOG_FILE)
    db.create('db_log', list(metadata.keys()))
    db.populate('db_log', metadata)
    commited = get_commited(log)
    uncomitted = get_uncommited(log, commited)
    # print('---------------------------Before recovery------------------------')
    # print_table(list(metadata.keys()), db.selectAll())

    undo(log, uncomitted)
    for t in uncomitted: print(f'Transação {t} realizou UNDO')
    # print('---------------------------After undo------------------------')
    # print_table(list(metadata.keys()), db.selectAll())


    redo(log, commited)
    for t in commited: print(f'Transação {t} realizou REDO')


    # print('---------------------------After redo------------------------')
    print_table(list(metadata.keys()), db.selectAll())



        


  
    
