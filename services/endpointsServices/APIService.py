from fastapi import FastAPI
import uvicorn
import services.endpointsServices.routers.ticket_router as ticket_router
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from tools.Logging import Logging


load_dotenv()
app=FastAPI()
app.include_router(ticket_router.ticket_router, prefix="/api")

errorLog=Logging("C:\\")

@app.get("/")
def HealthCheck():
    return {"Message": "Web service is running"}


def runWebServer():
    try:
        port=int(os.getenv("WebServerPort","5055"))
        uvicorn.run(app,port=port,reload=False)
        return True
    except:
        errorLog.write("endPointService.txt","Web Sever not not running") 
        return False

    


if __name__=="__main__":
     runWebServer()
