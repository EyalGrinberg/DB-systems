from queries_db_script import get_query_as_text
import mysql.connector

def create_tables():
    fd = open('queries/createTable.sql', 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for comm in sqlCommands:
        try:
            cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437',
                                          db='eyalgrinberg', port=3305)
            cursor = cnx.cursor()
            cursor.execute(comm)
        except:
            continue


