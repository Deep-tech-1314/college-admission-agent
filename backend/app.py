from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import initialize_rag, query_agent
import uvicorn
from contextlib import asynccontextmanager

# Define request/response models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# Lifespan context manager for startup tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the RAG pipeline (loads vector db and LLM) on startup
    initialize_rag()
    yield

app = FastAPI(
    title="College Admission Agent API",
    description="RAG-powered API for answering college admission queries using IBM Granite.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask", response_model=QueryResponse, summary="Ask a question about college admissions")
async def ask_question(request: QueryRequest):
    """
    Submit a question to the RAG agent.
    The agent will retrieve relevant context from the admission data and use the IBM Granite model to formulate an answer.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    result = query_agent(request.question)
    return QueryResponse(
        answer=result.get("answer", ""),
        sources=result.get("sources", [])
    )

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
