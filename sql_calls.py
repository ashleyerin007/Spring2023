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

# list of university names; 5 most productive schools in terms of publications assoc w faculty

def top_schools():
    sql4 = '''
    SELECT DISTINCT university.name, COUNT(faculty_publication.publication_id) AS pubs
    FROM university
    JOIN faculty
    ON university.id = faculty.university_id
    JOIN faculty_publication
    ON faculty.id = faculty_publication.faculty_id
    GROUP BY university.name
    ORDER BY pubs DESC
    LIMIT 5;
    '''

    with engine.connect() as cnx:
        schools_list = pd.read_sql(sql4, cnx)

    #print(schools_list.name.tolist())

    return schools_list.name.tolist()


cursor.close()


if __name__ == '__main__':
    show_table()
    scatterp()
    get_list()
    top_schools()