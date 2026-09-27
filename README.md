# Ticket Box - AI Support Ticket System

A Python-based support ticket system that combines a FastAPI ticket API, MySQL persistence, and an Ollama-powered AI assistant with RAG-based knowledge retrieval.

## Overview

This project is designed to help manage support tickets while also allowing a conversational AI assistant to:

- list all tickets
- retrieve a specific ticket by ID
- create a new ticket
- ground responses in a local knowledge base using Chroma + RAG
- interact with the ticket API through tool calls

The system is organized into separate layers for the API, database access, repositories, services, AI logic, and supporting tools.

## Project Structure

```text
.
├── main.py
├── pyproject.toml
├── README.md
├── support_ticket_system_knowledge_base.txt
├── agents/
│   ├── __init__.py
│   ├── Oldcode.py
│   └── ollamaAgent.py
├── database/
│   ├── __init__.py
│   ├── myDb.py
│   └── mysqlDb.py
├── repositories/
│   ├── __init__.py
│   └── ticket_repository.py
├── services/
│   ├── AIServices/
│   │   ├── __init__.py
│   │   └── AIServiceMain.py
│   └── endpointsServices/
│       ├── __init__.py
│       ├── APIService.py
│       └── routers/
│           ├── __init__.py
│           └── ticket_router.py
├── TicketRAGDB/
│   ├── chroma.sqlite3
│   └── 5b6423db-7337-4505-b5b0-f3fbf33cf5da/
├── tools/
│   ├── __init__.py
│   ├── AgentTools.py
│   ├── ChormaRAG.py
│   └── Logging.py
└── .env
```

## Main Components

### API Layer

- `services/endpointsServices/APIService.py` starts the FastAPI application.
- `services/endpointsServices/routers/ticket_router.py` exposes ticket endpoints.

### Database Layer

- `database/mysqlDb.py` creates the MySQL connection.
- `database/myDb.py` tests the MySQL connection using environment variables.

### Repository Layer

- `repositories/ticket_repository.py` handles ticket CRUD logic.

### AI Layer

- `services/AIServices/AIServiceMain.py` initializes the Ollama model and connects the LLM with the ticket toolset.
- `tools/ChormaRAG.py` builds and queries a Chroma vector store for knowledge retrieval.
- `tools/AgentTools.py` wraps ticket functions for LLM tool calling.

### Entrypoint

- `main.py` launches the API service, database check process, and AI service together.

## Prerequisites

Before running the project, install:

- Python 3.13+
- uv package manager
- MySQL database server
- Ollama with a model available locally, such as a compatible LLM and embedding model

## Environment Variables

Create a `.env` file in the project root with values like:

```env
DBHost=localhost
DBName=ticket_system
DBUsr=root
DBPass=your_password

AIType=Ollama
LLM=llama3.1
RAGPath=TicketRAGDB
RAGCollectionName=ticket_support
API_BASE_URL=http://127.0.0.1:5055/api/tickets
doc_Path=support_ticket_system_knowledge_base.txt
WebServerPort=5055
```

> Adjust these values to match your local setup and running environment.

## Installation

```bash
uv sync
```

This installs the dependencies listed in `pyproject.toml`.

## Running the Project

Start the full application:

```bash
uv run main.py
```

This launches the service processes defined in `main.py`:

1. the API server
2. the database connection check
3. the AI assistant service

## API Endpoints

The FastAPI router exposes endpoints under `/api`:

- `GET /api/tickets` - list tickets
- `GET /api/tickets/{ticket_id}` - get one ticket
- `POST /api/tickets/newticket` - create a ticket
- `PUT /api/tickets/{ticket_id}` - update a ticket
- `DELETE /api/tickets/{ticket_id}` - delete a ticket

## AI Assistant Behavior

The AI assistant uses the Ollama model and the ticket tools to support ticket-related interactions. It can:

- answer questions grounded in the local knowledge base
- call functions such as listing or creating tickets
- use knowledge retrieval when the `RAG` feature is enabled

## Knowledge Base

The project includes a knowledge text file:

- `support_ticket_system_knowledge_base.txt`

This file is used by the Chroma-based retrieval layer to provide document context for AI responses.

## Notes

- The project relies on `Ollama` and vector storage being available locally.
- The database and API must be reachable before the assistant can fully function.
- Some runtime behavior depends on the documents and environment variables being set correctly.

## Troubleshooting

If the app does not start correctly, check:

- MySQL is running and the credentials are valid
- Ollama is installed and the configured model is available
- `RAGPath` and `doc_Path` point to valid files/directories
- the FastAPI port is not already in use

## License

This project does not currently declare a specific license. Add one if you plan to distribute or publish the application.
