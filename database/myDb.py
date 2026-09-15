from mysqlDb import mysqlDb
import mysql.connector
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

def myDBtesting():
    try:
        Host= os.getenv("DBHost") 
        
        DBName=os.getenv("DBName")
        DbUsr=os.getenv("DBUsr")
        DbPass=os.getenv("DBPass")
        connection = mysqlDb(Host=Host, DBName=DBName, DbUser=DbUsr, DbPass=DbPass).get_connection()
        if connection.is_connected():
           
            print(f"DB connected")
            return  connection
        else:
            raise ValueError(f"Db is not connected")
    
    except Exception:
        raise ValueError(f"Db connection issue")

if __name__=="__main__":
    myDBtesting()