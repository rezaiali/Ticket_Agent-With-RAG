import os
from pathlib import Path 

class Logging:
    def __init__(self,_path:str):
    
         self._path=_path

    @property
    def currentPath(self):
        return self._path

    @currentPath.setter
    def currentPath(self,value:str):
        if value==None or value.join("")=="":
            raise ValueError("Path can't be empty!")
        self._path=value

    def write(self,fileName,content):
        try:

            writingFile = Path(self._path) / fileName

            if writingFile.exists():
                with open(writingFile, "a") as loggingfile:
                    loggingfile.writelines(content)
            else:
                with open(writingFile, "w") as loggingfile:
                    loggingfile.writelines(content)
            return True
        except SystemError:
            return False

    def read(self,fileName):
        readingFile = Path(self._path) / fileName

        if not readingFile.exists():
            raise FileNotFoundError(f"File not found: {readingFile}")

        with open(readingFile, "r") as loggingfile:
            return loggingfile.read()
