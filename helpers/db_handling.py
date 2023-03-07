from config import CONN, ENGINE


import pandas.io.sql as psql

def client_list():
    df = psql.read_sql(f"SELECT * FROM client_list WHERE active = 1",con = ENGINE)
    return df

def credentail(value):
    df = psql.read_sql(f"SELECT * FROM cred_test WHERE name = '{value}'",con = ENGINE)
    return df

def authentication(value):
    df = psql.read_sql(f"SELECT * FROM br_auth_params WHERE email = '{value}'",con = ENGINE)
    return df














# def db_connect():
#     cursor = CONN.cursor()
#     return cursor

# def client_list():
#     connection = db_connect()
#     connection.execute('''SELECT * FROM client_list''')
#     results = connection.fetchall()
#     return results


    