import requests as r
from requests.exceptions import HTTPError
import json
import pymysql.cursors
import sqlalchemy
from sqlalchemy import MetaData, Integer, String, DateTime, Column, Table
import pandas as pd
import os

apiurl = "https://journal.bsuir.by/api/v1/"
tablename = 'studentsdata'
mysqluser = 'root'
password = 'password'
ip = 'localhost'
database = 'unidata'
faculty = 'ФИК'


def get_info(apitype):
    try:
        response = r.get(apiurl + apitype)
        response.raise_for_status()
        # print(response.text)
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_fac_id(name):
    '''получить id факультета'''
    faculties = get_info("faculties")
    for fac in faculties:
        if fac['abbrev'] == name:
            return fac["id"]
    return None


def filter(groups, id):
    for group in groups:
        if group["facultyId"] == id:
            yield group


def get_groups(fac_id):
    '''получить id групп'''
    fac_groups = []
    groups = get_info("groups")
    for fic_group in filter(groups, fac_id):
        fac_groups.append(fic_group)
    return fac_groups


# 2 группы, которых не было
# for gr in groups:
#     if gr['id'] in (22233, 22648):
#         print(f"id - {gr['id']}: num - {gr['name']}")
# id - 22648: num - 860802
# id - 22233: num - 761402

def get_data(groups):
    '''save data'''
    for group in groups:
        group_id = group["id"]
        data = get_info(f"studentGroup/schedule?id={group_id}")
        with open(f'data_{group_id}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)


def create_table(engine, name):
    '''create mysql table'''
    metadata = sqlalchemy.MetaData()
    name = Table(
        name, MetaData,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('dayweel', String),
        Column('numberweek', Integer),
        Column('lesson', String),
        Column('typelesson', String),
        Column('class', String),
        Column('time', DateTime)
    )
    metadata.create_all(engine)


def create_table(connection, name):
    with connection.begin():
        metadata = sqlalchemy.MetaData()
        name = Table(
            name, metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(length=15)),
            Column('weekday', String(length=15)),
            Column('numberweek', Integer),
            Column('subject', String(length=30)),
            Column('typelesson', String(length=10)),
            Column('class', String(length=15)),
            Column('time', DateTime)
        )
        metadata.create_all(connection)


def get_data2(groups):
    '''save data'''
    for group in groups:
        group_id = group["id"]
        data = get_info(f"studentGroup/schedule?id={group_id}")

        print(type(data))
        print(data)

        data = pd.json_normalize(data)
        data.get('studentGroup')
        print(data)
        break


if __name__ == "__main__":
    # get data from API
    fac_id = get_fac_id(faculty)
    groups = get_groups(fac_id)
    # get_data(groups)

    engine = sqlalchemy.create_engine(
        f'mysql+pymysql://{mysqluser}:{password}@{ip}/{database}', echo=True)
    create_table(engine.connect(), name=tablename)

    # data_list = []
    # for file in os.listdir('./data'):
    # #If file is a json, construct it's full path and open it, append all json data to list
    #     if 'data_22232.json' in file:
    #         with open (f'data/{file}'):
    #         # json_path = os.path.join(os.getcwd(), 'data', file)
    #         # json_data = pd.read_json(json_path, orient='records')
    #             data = json.load(file)
    #             print(pd.json_normalize(data))

    # print(data_list)
    get_data2(groups)

    
    # for file in os.listdir('./data'):
    #     if 'json' in file:

    #     os.getcwd
    #     with open(f'data/{file}', 'r'):
    #         data = json.load(f'data/{file}')
    #         print(json.dumps(data, indent=2))
    #         # data.head()
    #     break


# Расписание индивидуальных групп
# for gr_id in data.keys():
#     resp = r.get("https://journal.bsuir.by/api/v1/studentGroup/schedule?id={}".format(gr_id)).json()
#     print(resp)
#     break

# # Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='password',
#                              db='TESTIMPORT',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO monday ('group_id', 'group_name', 'Aud', 'Subj', 'Teacher') VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(sql, ('22862', '863011', "506-3", "ПСИС", "Прищепа С. Л. (Профессор)"))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     # with connection.cursor() as cursor:
#     #     # Read a single record
#     #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#     #     cursor.execute(sql, ('webmaster@python.org',))
#     #     result = cursor.fetchone()
#     #     print(result)
# finally:
#     connection.close()
