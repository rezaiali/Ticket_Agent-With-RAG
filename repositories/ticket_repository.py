from database.mysqlDb import mysqlDb
import mysql.connector

class ticketRepo():
    def __init__(self):
        self.connected=False
    
    def __getConnect(self):
        try:
            return mysqlDb().get_connection()
        except Exception:
            raise ValueError(f"Db connection issue")
        
    def getAllTickets(self):
        with self.__getConnect() as conn:
            with conn.cursor() as cursor:
                 cursor.execute("""
                    SELECT ticket_id, title, description, status, category
                    FROM tickets
                    ORDER BY ticket_id;
                """)

            return cursor.fetchall()
            
