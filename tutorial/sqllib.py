#!/usr/bin/python3

import sqlite3
from functools import reduce

class DB_Exec(sqlite3.Cursor):

    def insert_data(self,database_name,lists):

        execute_str = "insert or replace into " + database_name + " values (" + \
                  reduce(lambda str1,str2:str1+','+str2, (map(lambda elem:repr(elem) \
                  if isinstance(elem,str) else str(elem),lists))) + ")"

        print("Execute SQL command ==> %s " % execute_str)
        self.execute(execute_str)

    def check_in_database(self,table_name,id_name,str_value):

        execute_str = "select * from %s where %s='%s'" % (table_name,id_name,str(str_value))

        print("Execute SQL command ==> %s " % execute_str)
        self.execute(execute_str)
        return(self.fetchall())

    def check_num_in_database(self,table_name,id_name,str_value):

        execute_str = "select count(*) from %s where %s='%s'" % (table_name,id_name,str(str_value))

        print("Execute SQL command ==> %s " % execute_str)
        self.execute(execute_str)
        return(self.fetchall()[0][0])

    def create_table(self,database_name,lists):

        execute_str = "create table if not exists " + database_name + " (" + \
                        reduce(lambda str1,str2:str1+','+str2,lists) + ")"

        print("Execute SQL command ==> %s " % execute_str)
        self.execute(execute_str)

    def delete_table(self,database_name):

        execute_str = "drop table if exists %s" % database_name

        print("Execute SQL command ==> %s " % execute_str)
        self.execute(execute_str)

if __name__ == '__main__':
    database_name = 'test_database'
    conn = sqlite3.connect('test.db')
    c = conn.cursor(DB_Exec)
    c.create_table(database_name,('id int primary key','title text','author text','time int'))
    conn.commit()
    #test create database twice
    c.create_table(database_name,('id int','title text','author text','time int'))
    conn.commit()
    #insert data test
    c.insert_data(database_name,(123,'234','232',345))
    c.insert_data(database_name,(32,'test','hello',345))
    c.insert_data(database_name,(99,'234','sdfsda',345))
    c.insert_data(database_name,(99,'error','test',666))
    print(c.fetchall())
    c.insert_data(database_name,(332,'test2','hello',3345))
    print(c.fetchall())
    conn.commit()
    #select command test
    print(c.check_in_database(database_name,'id',32))
    print(c.check_in_database(database_name,'id',333))
    print(c.check_in_database(database_name,'id',99))
    print(c.check_in_database(database_name,'author','hello'))
    print(c.check_num_in_database(database_name,'id',32))
    print(c.check_num_in_database(database_name,'title',234))
    print(c.check_num_in_database(database_name,'author','hello'))
    print(c.check_num_in_database(database_name,'id',33))
    c.delete_table(database_name)
    conn.commit()
    conn.close()	
