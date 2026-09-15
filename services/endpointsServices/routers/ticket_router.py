from fastapi import APIRouter
from repositories.ticket_repository import ticketRepo

ticket_router=APIRouter()

@ticket_router.get("/tickets")
def getTickets():
    return {"message": f"The list of all tickets {ticketRepo().getAllTickets()}"}



