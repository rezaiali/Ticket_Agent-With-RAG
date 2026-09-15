from fastapi import APIRouter
from repositories.ticket_repository import ticketRepo

ticket_router=APIRouter()

@ticket_router.get("/tickets")
async def getTickets():
    ticketlist = await ticketRepo().getAllTickets()
    return {"message": f"The list of all tickets {ticketlist}"}



