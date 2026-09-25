from agents.ollamaAgent import OllamaAgent
from tools.ChormaRAG import ChromaRAG
from langchain_ollama.embeddings import OllamaEmbeddings
from tools.Logging import Logging
from pathlib import Path
from dotenv import load_dotenv
import shutil
import os
import sys

class AIServiceMain():
    def __init__(self,Type:str,LLMmodel:str,RAGDocPath:str="", DBNname:str="", useRAG=False):

        self.additionalInfo=""
        self.question=""
        
        self.result=""

        match Type:
            case "Ollama":
                ollamaLLM=OllamaAgent(LLMmodel)
                if useRAG:
                    embedding=OllamaEmbeddings(model="mxbai-embed-large")
                    theRAG= ChromaRAG(DBNname,RAGDocPath,embedding)
                    theRAG.createChromaVectorStore()
                    Infos=theRAG.retiever(4).invoke(self.question)

                    for addinfo in Infos:
                         self.additionalInfo=" ".join(addinfo.page_content)

                
                    
            case "_":
                pass
        
        #return self.result

def runAIService():
    errorLog=Logging("C:\\")

    load_dotenv()
    AIType=str(os.getenv("AIType"))
    LLM=str(os.getenv("LLM"))
    #RAGPath=str(os.getenv("RAGPath"))
    VCDBFolder=Path("./TicketRAGDB")
    try:
        if VCDBFolder.is_dir():
           shutil.rmtree(VCDBFolder)
 
        AIServiceMain(AIType, LLM, "./TicketRAGDB","ticket_rag",True)

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break
            if not user_input:
                continue

        return True
    except Exception as err:
        exc_type, exc_value, exc_tb = sys.exc_info()

        # exc_tb can be None when the exception context is unavailable.
        line_number = exc_tb.tb_lineno if exc_tb is not None else -1

        print(f"execption:: {err} (line {line_number})")
        errorLog.write("endPointService.txt","Web Sever not not running") 
        return False

if __name__=="__main__":
     runAIService()
   