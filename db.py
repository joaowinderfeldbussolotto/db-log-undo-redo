import psycopg2
from decouple import config


DATABASE = config('DB_NAME')
HOST = config('DB_HOST')
USER = config('DB_USER')
PASSWORD = config('DB_PASSWORD')
PORT = config('DB_PORT')

class DB:


    def exec(self, sql):
        print(sql)
        con = None
        result = None

        try:
            con = psycopg2.connect(dbname=DATABASE,host=HOST,user= USER,password= PASSWORD,port= PORT)
            cur = con.cursor()
            cur.execute(sql)

            if cur.pgresult_ptr is not None:
                result = cur.fetchall()
            cur.close()
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
            return result




    
    def create(self, name : str, columns : list):
        drop_table_if_exists_query = f"DROP TABLE IF EXISTS {name};"
        self.exec(drop_table_if_exists_query)
        create_query = f"CREATE TABLE IF NOT EXISTS {name} ("
        
        # Percorre as colunas na lista de colunas e adiciona ela na create_query
        create_query+= 'id serial, '
        for column in columns:
            column = str(column)
            create_query += column + " varchar(4000)" + ( "," if (column != columns[-1]) else "" )
        
        create_query += " );"


        
        self.exec(create_query)
        
        
    
    
    def populate(self, table_name : str = 'db_log', data : dict = {}):
        

        columns = ','.join(data.keys())

        # Flatten the lists of values and convert them to strings
        flattened_values = [str(tuple(item)) for item in zip(*data.values())]

        insert_query = f"INSERT INTO db_log ({columns}) VALUES {','.join(flattened_values)};"
        
        # Executando a query para inserção
        self.exec(insert_query)

    def update(self,id, col, val):
        self.exec(f'UPDATE log set {col}={val} WHERE id={id}')
        
        