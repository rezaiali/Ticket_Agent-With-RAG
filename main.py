import subprocess
import sys
import time
from datetime import datetime
from tools.Logging import Logging


def main():
    
    servicesLogs= Logging("C:\\")

  
    processServices = subprocess.Popen([sys.executable, "-m",'services.endpointsServices.APIService'])
    processDB = subprocess.Popen([sys.executable, './database/myDb.py'])
    processAI=subprocess.Popen([sys.executable,"-m",'services.AIServices.AIServiceMain'])

    
    now =datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    print("Both scripts are running in parallel...")
    
    servicesLogs.write("serviceLogs.txt",f"\n {timestamp}:: Both scripts are running in parallel...\n -------")


    processServices.wait()
    time.sleep(2.5)
    processDB.wait()

    print("Both scripts have finished.")
    servicesLogs.write("serviceLogs.txt",f"\n {timestamp}:: Both scripts have finished.\n-------")


if __name__ == "__main__":
        main()
