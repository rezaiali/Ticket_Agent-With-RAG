from database.mysqlDb import mysqlDb
import mysql.connector
import asyncio
import os
from dotenv import load_dotenv
import json

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
            if connection.is_connected():
                return  connection
            else:
                raise ValueError(f"Db is not connected")
        
        except Exception as error:
            raise ValueError("Database connection issue") from error
        
    def _getAllTickets_sync(self):
         with self.__getConnect() as conn:
             if conn.is_connected():
                cur= conn.cursor(dictionary=True)
                cur.execute("Select * from tickets")
                tickets = cur.fetchall()
                cur.close()
                return tickets
             else:
                 raise ValueError(f"Db is not connected")

    def _getTicket_sync(self, ticket_id):
        try:
            with self.__getConnect() as conn:
                if conn.is_connected():
                    cur=conn.cursor(dictionary=True)
                    cur.execute("""
                    SELECT *
                    FROM tickets
                    WHERE ticket_id = %s;
                """, (ticket_id,))
                    theticket= cur.fetchone()
                    cur.close()
                return  theticket
        except Exception as error:
             
             return  {"message":f"there was an issue:: {error}"}
    def _createTicket_sync(self,ticket):
        try:
            with self.__getConnect() as conn:
                cur=conn.cursor(dictionary=True)
                cur.execute(
                    """INSERT INTO tickets (title, description, status, category)
                       VALUES (%s, %s, %s, %s)""",
                    (ticket["title"], ticket["description"], "new", ticket["category"]),
                )
                conn.commit()
                cur.close()
                return True
        except Exception as error:
            
            return False
        
    def _updateTicket_sync(self,ticket_id,ticket):
        try:
            with self.__getConnect() as conn:
                cur=conn.cursor(dictionary=True)
                cur.execute("""
                        UPDATE tickets
                        SET title =%s,
                        description =%s,
                        status = %s,
                        category = %s
                        WHERE ticket_id = %s
                    """, (
                        ticket["title"],
                        ticket["description"],
                        ticket["status"],
                        ticket["category"],
                        ticket_id
                    ))

                conn.commit()
                updated_ticket = cur.rowcount
                cur.close()
            return updated_ticket
        except Exception as error:
             return {"message": f"An unexpected error occurred: {error}"}

    def _deleteTicket_sync(self, ticket_id):
        try:
            with self.__getConnect() as conn:
                cur=conn.cursor(dictionary=True)
                cur.execute("""
                    DELETE FROM tickets
                    WHERE ticket_id = %s
                """, (ticket_id,))
                conn.commit()
                deleted_ticket = cur.rowcount
                cur.close()
                return deleted_ticket
        except Exception as error:
            return {"message": f"An unexpected error occurred: {error}"}


    async def getAllTickets(self):
        return  await asyncio.to_thread(self._getAllTickets_sync)
    async def getTicket(self,Ticket_id):
            return await asyncio.to_thread(self._getTicket_sync, Ticket_id)
    async def createTicket(self,Ticket):
            return  await asyncio.to_thread(self._createTicket_sync,Ticket)
    async def updateTicket(self,ticket_id, Ticket):
            return  await asyncio.to_thread(self._updateTicket_sync, ticket_id, Ticket)
    async def deleteTicket(self,ticket_id):
            return  await asyncio.to_thread(self._deleteTicket_sync, ticket_id)
    
    
            
