from django.db import connection





def SelectEx(table,where=''):
    with connection.cursor() as cursor:
        if where == '':
            cursor.execute(f"SELECT * FROM {table}")
        else:
            cursor.execute(f"SELECT * FROM {table} WHERE {where}")
        rows = cursor.fetchall()
    return rows

def InsertEx(table,key,value):
    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table} ({key}) VALUES ({value})"
            cursor.execute(sql)
            cursor.connection.commit()
            return True
    except:return False

def UpdateEx(table,keyValue,where=''):
    try:
        with connection.cursor() as cursor:
            if where == '':
                sql = f"UPDATE {table} SET {keyValue}"
            else:
                sql = f"UPDATE {table} SET {keyValue} WHERE {where}"
            cursor.execute(sql)
            cursor.connection.commit()
            return True
    except:
        return False



def DeleteEx(table,where):
    try:
        with connection.cursor() as cursor:
            sql = f"DELETE FROM {table} WHERE {where}"
            cursor.execute(sql)
            cursor.connection.commit()
            return True
    except:return False