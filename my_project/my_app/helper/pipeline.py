import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import psycopg2 as pg

src_db = "/home/mamisoa/Documents/Mamisoa_Rasolofondraibe/Projet python/Framework python/django_project2/db (1).sqlite3"
src_connexion = sqlite3.connect(src_db)
target_db = {
        'name': 'django',
        'user': 'postgres',
        'psswd': 'pgsql69!',
        'host': 'localhost',
        'port': '5432',
}
def extract():
    try:
        cursor = src_connexion.cursor()
        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name in ('my_app_medicine', 'my_app_symptome', 'my_app_medicinesymptome')""")
        src_table = cursor.fetchall()

        for table in src_table:
            dataFrame = pd.read_sql_query(f'SELECT * FROM {table[0]}', src_connexion)
            load (dataFrame, table[0])
    except Exception as e:
        print("Data extract error: "+str(e))

def load(dataFrame, tableName):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{target_db["user"]}:{target_db["psswd"]}@{target_db["host"]}:{target_db["port"]}/{target_db["name"]}')
        ##with engine.connect() as connection:
            ##connection.execute(f'SELECT * FROM {tableName}')
        print(f'Importing rows {rows_imported} to {rows_imported + len(dataFrame)} ... for table {tableName}')
        dataFrame.to_sql(f'{tableName}', engine, if_exists='append', index=False)
        rows_imported += len(dataFrame)
        print('Data imported successfully')
        engine.dispose()
    except Exception as e:
        print("Data load error: "+str(e))


try:
    extract()
except Exception as e:
    print('An error occured during operations '+ str(e))

