import pymysql
from pymysql import cursors
from config import *

try:
    connection = pymysql.connect(
        host=host,
        port=8889,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('Successfully connected ...')
    print('#' * 20)

    # to know what time free
    def get_empty_space(client_date: list):

        get_client_time = '"' + '-'.join(client_date) + '"' # ['2023', '01', '26'] -> "2023-01-26"

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `calendar` WHERE data = {get_client_time}")
            info = cursor.fetchall()  # check what type (tuple or list)

            if isinstance(info, tuple):  # if do not have this day in database -> create new day in database
                with connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO `calendar` (data) VALUES ({get_client_time})")
                    connection.commit()
                return get_empty_space(client_date) # restart func

            elif isinstance(info, list):  # if we already have day in database
                # cheking what time is free | Null = free , 1 = already took
                space_first = False if info[0]['T14'] == '1' else True
                space_second = False if info[0]['T15'] == '1' else True
                space_third = False if info[0]['T16'] == '1' else True
                return [space_first, space_second, space_third] # True = free cell, False = already took

    # to took cell in day | 0 -> 1
    def update_data(client_time: list, client_date: list):
        time = f"T{client_time[0]}" # 16 -> T16
        get_client_time = '"' + '-'.join(client_date) + '"' # ['2023', '01', '26'] -> "2023-01-26"
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE `calendar` SET {time} = '1' WHERE data = {get_client_time};") # free -> already took
            connection.commit()

    # Free Cell 1 -> 0
    def put_away_cell(date_for_sql: list):  # date_for_sql = ['2022-12-11', 'T15']
        date = f'"{date_for_sql[0]}"'  # '"2022-12-11"'
        time = date_for_sql[1]  # 'T15'
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE `calendar` SET {time} = '0' WHERE data = {date};") # already took -> free
            connection.commit()

except Exception as ex:
    print('Connection refuse ...')
    print(ex)


