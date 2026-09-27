import requests
import json
from dotenv import load_dotenv
import os


class AgentTools:
    def __init__(self):
        self.__TOOL_SCHEMAS=None

        self.API_BASE_URL=str(os.getenv("API_BASE_URL"))

    def list_of_tickets(self):
        try:
            response = requests.get(self.API_BASE_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            return json.loads(data) if isinstance(data, str) else data
        except requests.RequestException as error:
            return {"error": f"There was an issue getting tickets: {error}"}
        except json.JSONDecodeError as error:
            return {"error": f"The ticket service returned invalid data: {error}"}


    def find_ticket(self,ticket_id: int):
        try:
            response = requests.get(f"{self.API_BASE_URL}/{ticket_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            return {"error": f"There was an issue getting ticket {ticket_id}: {error}"}


    def create_ticket(self,title: str, description: str, category: str):
        payload = {
            "title": title,
            "description": description,
            "category": category,
            "status": "new",
        }
        try:
            response = requests.post(f"{self.API_BASE_URL}/newticket", json=payload, timeout=10)
            response.raise_for_status()
            try:
                return {"status_code": response.status_code, "ticket": response.json()}
            except ValueError:
                return {"status_code": response.status_code, "message": "Ticket created successfully."}
        except requests.RequestException as error:
            return {"error": f"There was an issue creating the ticket: {error}"}

    def get_tool_result(self, function_name: str, **arguments):
        if function_name == "ticket_list":
            return self.list_of_tickets()
        if function_name == "find_ticket":
            return self.find_ticket(**arguments)
        if function_name == "create_ticket":
            return self.create_ticket(**arguments)
        return {"error": f"Unknown tool: {function_name}"}


    @property 
    def TOOL_SCHEMAS(self) :
        return  [
        {"type": "function", "function": {"name": "ticket_list", "description": "List all tickets.", "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"type": "function", "function": {"name": "find_ticket", "description": "Find a specific ticket by its ID.", "parameters": {"type": "object", "properties": {"ticket_id": {"type": "integer", "description": "The ticket ID."}}, "required": ["ticket_id"]}}},
        {"type": "function", "function": {"name": "create_ticket", "description": "Create a support ticket when title, description, and category are known.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}, "category": {"type": "string", "description": "For example software, application, hardware, network, or customer."}}, "required": ["title", "description", "category"]}}},
    ]




# def get_tool_result(function_name: str, **arguments):
#     if function_name == "ticket_list":
#         return list_of_tickets()
#     if function_name == "find_ticket":
#         return find_ticket(**arguments)
#     if function_name == "create_ticket":
#         return create_ticket(**arguments)
#     return {"error": f"Unknown tool: {function_name}"}
