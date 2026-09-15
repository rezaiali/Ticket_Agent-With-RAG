import mysql.connector

class mysqlDb():
    def __init__(self,Host,DBName,DbUser,DbPass):
        #self._host= os.getenv("DBHost") #"localhost"
        self._host=Host
        #self._DBName=os.getenv("DBName")
        self._DBName=DBName
        #self._dbUsr=os.getenv("DBUsr")
        self._dbUsr=DbUser
        #self._dbPass=os.getenv("DBPass")
        self._dbPass=DbPass

    @property
    def host(self):
        return self._host
    
    @host.setter
    def getHost(self,value):
        self._host=value

    @property
    def DatabaseName(self):
        return self._DBName
    
    @host.setter
    def getDatabaseName(self,value):
        self._DBName =value
    @property
    def DbUser(self):
        return self._dbUsr
    
    @host.setter
    def getDbUser(self,value):
        self._dbUsr=value

    @property
    def DbPassword(self):
        return self._dbPass
    
    @host.setter
    def getDbpassword(self,value):
        self._dbPass=value

    def get_connection(self):
        return  mysql.connector.connect(
            host=self._host,
            database=self._DBName,
            user=self._dbUsr,
            password=self._dbPass
        )