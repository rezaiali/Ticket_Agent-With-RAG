from fastapi import APIRouter
from repositories.ticket_repository import ticketRepo

ticket_router=APIRouter()

@ticket_router.get("/tickets")
async def getTickets():
    ticketlist = await ticketRepo().getAllTickets()
    return {"message": f"The list of all tickets {ticketlist}"}

@ticket_router.get("/tickets/{ticket_id}")
async def getTicket(ticket_id:str):
    try:
        if ticket_id.strip()=="" or ticket_id==None:
            return {"mssages": "Ticket id issue!"}
        else:
            
            return await ticketRepo().getTicket(int(ticket_id))
    except (TypeError, ValueError):
        return {"message": "Ticket can not be found!"}


@ticket_router.post("/tickets/newticket")
async def createTicekt(newTicket:dict):
    createdTicket=await ticketRepo().createTicket(newTicket)
    print(createdTicket)
    if createdTicket:
        return {"mssages": "Ticket is created"}
    else:
        return {"mssages": "Ticket creation had an issue!"}
    
@ticket_router.put("/tickets/{ticket_id}")
async def updateTicket(ticket_id:str,newTicket:dict):
    try:
        if ticket_id.strip()=="" or ticket_id==None:
            return {"mssages": "Ticket id issue!"}
        else:
            
            updated=await ticketRepo().updateTicket(ticket_id,newTicket)
            return updated
    except (TypeError, ValueError):
        return {"message":"Ticket has NOt been updated!"}

@ticket_router.delete("/tickets/{ticket_id}")
async def deleteTicket(ticket_id):
    try:
        if ticket_id.strip()=="" or ticket_id==None:
            return {"mssages": "Ticket id issue!"}
        else:
            ticket=await ticketRepo().deleteTicket(ticket_id)
            return {"message": f" the ticket {ticket} has been deleted"}
    except (TypeError, ValueError):
        return {"messgae": f"The ticket {ticket_id} hasn't been removed!"}

