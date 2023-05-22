import json
from db import DB

def getMetadata(metadata_file):
    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
    return metadata['INITIAL']

def load_log(log_file):
    with open(log_file, 'r') as file:
        log_data = file.read().splitlines()
    return log_data

#Se não tem commmit, segue


if __name__ == '__main__':
    db = DB()
    metadata_file = 'metadado.json'
    log_file = 'entradaLog(1)'
    metadata = getMetadata(metadata_file)
    log = load_log(log_file)
    print(metadata)
    db.create('db_log', list(metadata.keys()))
    print(metadata)
    db.populate('db_log', metadata)


    # for key, value in metadata.items():  
    #     db.populate(key, value) 
        


  
    
