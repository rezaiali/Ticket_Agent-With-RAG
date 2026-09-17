import os
import json
import requests
import subprocess

from dotenv import load_dotenv

from ollama import chat
from ollama import ChatResponse



load_dotenv()

apiHost=os.getenv("APIHost")

model= "aleshribar3/deepseek-r1-tool-calling"

messages=[]

SYSTEM_PROMPT = """
You are an AI agent that helps users interact with an issue ticket system.
show the user list of ticket that exisit tickets and
when the user can asks to show a ticket with a number, you take the number as ticket id, find the ticket
and show the ticket to the user
when the user ask to create a new ticket, before calling the tool, ask the user what is the 'title', 'description' 
and the category of the ticket, if the user give you all three item, then create a ticket, otherwise, 
tell the user you cant create a ticket
"""   

def list_of_tickets():
    try:
        response = requests.get(
            f"{apiHost}api/tickets",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, str):
                data = json.loads(data)

            return data

        else:
            return {
                "error": "There were no tickets"
            }

    except Exception as e:
        return {
            "error": f"There was an issue getting the tickets: {str(e)}"
        }


def find_ticket(arg):
    
   try:
      ticket_id=arg["ticket_id"]
      print(f"theTicket", ticket_id) 
      response=requests.get(f"{apiHost}{ticket_id}",timeout=10)
      if response.status_code == 200:
            data = response.json()
            return data
      
      else:
        return {
         "error": f"There was an error There were no tickets {response.status_code}"
            }
      
          
   except Exception as e:
              return {
                  "error": f"There was an issue getting the tickets: {str(e)}"
              }

def create_ticket():
    newticket = {
        "title": "",
        "description": "",
        "category": ""
    }
    while not newticket["title"]:
        newticket["title"] = input("What is the title: ").strip()
    
    while not newticket["description"]:
        newticket["description"] = input("What is the description: ").strip()

    while not newticket["category"]:
            newticket["category"] = input("What is the category: ").strip()

    payload={
        "title": newticket["title"],
        "description": newticket["description"],
        "category": newticket["category"],
        "status": "new"
    }
    headers={
        "Content-Type": "application/json"
    }
    try:
   
        response = requests.post(f"{apiHost}api/tickets/newticket", json=payload, headers=headers, timeout=10)
    
   
        response.raise_for_status()
    
   
         
        return response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        #print(f"HTTP error occurred: {http_err}")  # e.g., 404 or 500 errors
        return {"error":http_err}
    except requests.exceptions.ConnectionError as conn_err:
        #print(f"Connection error occurred: {conn_err}")
        return {"error":conn_err}
    except requests.exceptions.Timeout as timeout_err:
        #print(f"The request timed out: {timeout_err}")
        return {"error":timeout_err}
    except requests.exceptions.RequestException as err:
        #print(f"An error occurred: {err}")
        return {"error": err}


def getToolResult(functionname:str,**kwargs):
    match(functionname):
        case "ticket_list":
            return list_of_tickets()
        case "find_ticket":
            return find_ticket(kwargs)
        case "create_ticket":
            return create_ticket()

TOOLS= {
    "ticket_list": "ticket_list",
    "find_ticket": "find_ticket",
    "create_ticket":"create_ticket"
}

TOOL_SCHEMAS=[
    
    {"type": "function", 
     "function": {
         "name": "ticket_list",
         "description": "Call this tool whenever the user asks to list, show, display, or get all tickets.",
         "parameters": {
            "type": "object",
            "properties": {},
            "required": []
            }
     }},
     {
        "type":"function",
        "function":{
            "name":"find_ticket",
            "description": "find a specific ticket using the ticket id",
            "parameters": {
               "type": "object",
                "properties": {"ticket_id":{
                    "type":"integer",
                    "description": "The ID of the ticket"
                 }
                },
                "required": ["ticket_id"]
            }
        }
     },
     {
         "type":"function",
         "function": {
             "name":"create_ticket",
             "description": "create a new ticket",
             "parameters": {
                 "type":"object",
                 "properties": {
                     "title": {
                        "type":"string",
                        "description": "the title of the issue"
                     },
                     "description": {
                          "type":"string",
                          "description": "details about the issue"
                          },
                      "category": {
                          "type":"string",
                          "description": "should one of these: 'software', 'application', 'hardware', 'network' and 'customer'"
                      }
                      
                 },
                 "required": ["title","description","category"]
             }
         }
     }
]