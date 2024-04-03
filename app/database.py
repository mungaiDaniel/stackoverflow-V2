import os  
import datetime
import psycopg2

class MY_DATABASE:
    
    
    def connect_to_db():
        
        connect = psycopg2.connect(os.environ['DATABASE_URL'])
        connect.autocommit = True
        cursor = connect.cursor()
        
        return cursor
    
    
    def create_questions_table():
        '''function to create questions table'''
        cursor = MY_DATABASE.connect_to_db()
        sql_command = """CREATE TABLE IF NOT EXISTS "public"."questions"  (
        id SERIAL ,
        title VARCHAR(255) NOT NULL,
        body VARCHAR(1000) NOT NULL,
        user_id INTEGER NOT NULL,
        date_created VARCHAR(80),
        date_modified VARCHAR(80),
        PRIMARY KEY (id),
        FOREIGN KEY (user_id)
        REFERENCES users (id)
            )"""
            
        cursor.execute(sql_command)



    def create_answers_table():
        '''function to create answers table'''
        cursor = MY_DATABASE.connect_to_db()
        sql_command = """ CREATE TABLE IF NOT EXISTS "public"."answers"  (
                id SERIAL ,
                body VARCHAR(400) NOT NULL,
                question_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,            
                date_created VARCHAR(80),
                date_modified VARCHAR(80),
                accept BOOLEAN  default FALSE,
                PRIMARY KEY (id),
                FOREIGN KEY (question_id)
                REFERENCES questions (id),
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    )"""
        cursor.execute(sql_command)


    def create_users_table():
        '''function to create questions table'''
        cursor = MY_DATABASE.connect_to_db()
        sql_command = """CREATE TABLE IF NOT EXISTS "public"."users"  (
        id SERIAL ,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        date_created VARCHAR(80),
        date_modified VARCHAR(80),
        PRIMARY KEY (id)
            )"""
        cursor.execute(sql_command)
        
    def save(self,format_str ):
        '''method to save to db'''
        cursor = MY_DATABASE.connect_to_db()
        
        try:
            cursor.execute(format_str)
        except:
            #log error
            return {
                "success":False,
                "error":"error"
            }
        return {
            "sucess": True,
            "message": "sucessfully save to db"
        }


    def drop_questions_table():
        '''function to drop questions table'''
        cursor = MY_DATABASE.connect_to_db()
        sql_command = """ DROP TABLE questions CASCADE;"""
        cursor.execute(sql_command)


    def drop_answers_table():
        '''function to drop answers table'''
        cursor =MY_DATABASE.connect_to_db()
        sql_command = """ DROP TABLE answers CASCADE;"""
        cursor.execute(sql_command)


    def drop_users_table():
        '''function to drop answers table'''
        cursor =MY_DATABASE.connect_to_db()
        sql_command = """ DROP TABLE users CASCADE;"""
        cursor.execute(sql_command)
        