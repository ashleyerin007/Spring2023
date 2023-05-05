import mysql.connector
import sqlalchemy as sa
from sqlalchemy import func
import pandas as pd

cnx = mysql.connector.connect(user='root',
                              password='test_root',
                              host='127.0.0.1',
                              database='academicworld')

cursor = cnx.cursor(buffered=True)

engine = sa.create_engine('mysql+mysqldb://root:test_root@127.0.0.1/academicworld')

def show_table():
    sql = '''
    SELECT DISTINCT name, position, university_id
    FROM faculty
    WHERE position = 'Professor'
    LIMIT 10;
    '''

    with engine.connect() as cnx:
        df = pd.read_sql(sql, cnx)

    #print(df)

    return df

    #cursor.close()

def scatterp():
    sql2 = '''
    SELECT name, id, COUNT(publication_keyword.keyword_id) AS frequency
    FROM keyword
    JOIN publication_keyword
    ON keyword.id = publication_keyword.keyword_id
    WHERE id IS NOT NULL
    GROUP BY name, id
    ORDER BY frequency DESC
    LIMIT 10;
    '''

    with engine.connect() as cnx:
        scatterdf = pd.read_sql(sql2, cnx)

    #print(scatterdf)
    
    return scatterdf

# returns list of journals (venues) publishing articles after 2015
def get_list():
    sql3 = '''
    SELECT DISTINCT venue
    FROM publication
    WHERE (year>2015)
    LIMIT 20;
    '''

    with engine.connect() as cnx:
        menu_list = pd.read_sql(sql3, cnx)

    #print(menu_list['venue'].tolist())
    
    return menu_list['venue'].tolist()

    cursor.close()


if __name__ == '__main__':
    show_table()
    scatterp()
    get_list()
