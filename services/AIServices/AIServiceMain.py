from ollama import chat
from tools.ChormaRAG import ChromaRAG
from langchain_ollama.embeddings import OllamaEmbeddings

from tools.Logging import Logging
from pathlib import Path
from tools.AgentTools import AgentTools
from dotenv import load_dotenv
import json
import shutil
import os
import sys

class AIServiceMain():
    def __init__(self,Type:str,LLMmodel:str,RAGDocPath:str="", DBNname:str="", useRAG=False):

        self.additionalInfo=""
        self.question=""
        self._LLModel=LLMmodel
        self.result=""
       
        
        # match Type:
        #     case "Ollama":
               
        if useRAG:
            embedding=OllamaEmbeddings(model="mxbai-embed-large")
            self.theRAG= ChromaRAG(DBNname,RAGDocPath,embedding)
            print (f" the doc:: {str(os.getenv("doc_Path"))}")
            self.theRAG.DocumentPath=str(os.getenv("doc_Path"))
            self.theRAG.createChromaVectorStore()
                  
                
                    
            # case "_":
            #     pass
        

    def _user_message_with_context(self, question: str,k=4) -> str:
        try:
            addinfos=self.theRAG.retiever(k).invoke(question)

            for addinfo in addinfos:
                result=" ".join(addinfo.page_content)
            
            return result
        except Exception as error:
            # Ticket tools remain usable if Ollama/the vector index is unavailable.
            context = f"Knowledge-base retrieval is currently unavailable: {error}"
        return f"Approved knowledge-base context:\n{context}\n\nUser request:\n{question}"


    def get_tool_result(self,function_name: str, **arguments):
        return AgentTools().get_tool_result(function_name,**arguments)



    def startLLM(self):

        SYSTEM_PROMPT = """
        You are an AI agent that helps users interact with an issue ticket system.

        Use the approved knowledge-base passages supplied with each question for
        general support guidance. Do not invent policies, ticket data, or technical
        instructions. If the passages do not answer the question, say so and suggest
        contacting a support agent.

        For ticket data, always use the available tools:
        - Use ticket_list when asked to list or show all tickets.
        - Use find_ticket with ticket_id when asked for a specific ticket.
        - To create a ticket, require title, description, and category. Ask for any
        missing fields; otherwise call create_ticket.
        - Never claim a ticket action succeeded unless its tool result confirms it.
        """.strip()




    
        print("Ticket assistant ready. Type 'exit' to quit.")
        messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
        toolsList=AgentTools().TOOL_SCHEMAS
        

    

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break
            if not user_input:
                continue

            messages.append({"role": "user", "content": self._user_message_with_context(user_input)})
            response = chat(model=self._LLModel, messages=messages, tools=toolsList)
            messages.append(response.message.model_dump(exclude_none=True))

            if response.message.tool_calls:
                for tool_call in response.message.tool_calls:
                    result = self.get_tool_result(tool_call.function.name, **tool_call.function.arguments)
                    messages.append({
                        "role": "tool",
                        "tool_name": tool_call.function.name,
                        "content": json.dumps(result, default=str),
                    })
                response = chat(model=self._LLModel, messages=messages, tools=toolsList)
                messages.append(response.message.model_dump(exclude_none=True))

            print(f"Assistant: {response.message.content}")



def runAIService():
    errorLog=Logging("C:\\")

    load_dotenv()
    AIType=str(os.getenv("AIType"))
    LLM=str(os.getenv("LLM"))
    RAGPath=str(os.getenv("RAGPath"))
    RAGCollection=str(os.getenv("RAGCollectionName"))
    VCDBFolder=Path(RAGPath)
    try:
        if VCDBFolder.is_dir():
           shutil.rmtree(VCDBFolder)
 
        AIServ=AIServiceMain(AIType, LLM, RAGPath,RAGCollection,True)
        AIServ.startLLM()
        

       
    except Exception as err:
        exc_type, exc_value, exc_tb = sys.exc_info()

        # exc_tb can be None when the exception context is unavailable.
        line_number = exc_tb.tb_lineno if exc_tb is not None else -1

        print(f"execption:: {err} (line {line_number})")
        errorLog.write("endPointService.txt","Web Sever not not running") 
        return False



if __name__=="__main__":
     runAIService()
    
   