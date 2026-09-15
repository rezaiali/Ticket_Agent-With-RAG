from database.mysqlDb import mysqlDb
import mysql.connector
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


class ticketRepo():
    def __init__(self):
        self.connected=False
    
    def __getConnect(self):
        try:
            Host= os.getenv("DBHost") 
            print("Host", Host)
            DBName=os.getenv("DBName")
            DbUsr=os.getenv("DBUsr")
            DbPass=os.getenv("DBPass")
            connection = mysqlDb(Host=Host, DBName=DBName, DbUser=DbUsr, DbPass=DbPass).get_connection()
            if connection.is_connected:
                return  connection
            else:
                raise ValueError(f"Db is not connected")
        
        except Exception:
            raise ValueError(f"Db connection issue")
        
    def _getAllTickets_sync(self):
         with self.__getConnect() as conn:
             if conn.is_connected:
                cur= conn.cursor(dictionary=True)
                cur.execute("Select * from tickets")
                tickets = cur.fetchall()
                cur.close()
                conn.close()
                return tickets
             else:
                 raise ValueError(f"Db is not connected")
    
    

    async def getAllTickets(self):
        
        return  await asyncio.to_thread(self._getAllTickets_sync)
            
