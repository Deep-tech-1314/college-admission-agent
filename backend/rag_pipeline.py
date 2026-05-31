import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings # Local embeddings if needed, but let's try to keep it simple, or use sentence_transformers directly
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# We use an open source local embedding model for simplicity and speed (no API key required for embeddings)
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

load_dotenv()

# IBM Cloud Configuration
IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

VECTOR_STORE_DIR = "./chroma_db"
DATA_FILE = "data/sample_admission_data.txt"

_qa_chain = None

def get_llm():
    if not IBM_CLOUD_API_KEY or not WATSONX_PROJECT_ID:
        # Fallback for local testing if keys are missing (Mocking the response)
        print("WARNING: IBM_CLOUD_API_KEY or WATSONX_PROJECT_ID not set. RAG pipeline will not initialize properly for production.")
        return None

    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 512,
        "min_new_tokens": 1,
        "repetition_penalty": 1.1
    }

    # Using IBM Granite model
    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-8b-code-instruct",
        url=WATSONX_URL,
        project_id=WATSONX_PROJECT_ID,
        apikey=IBM_CLOUD_API_KEY,
        params=parameters,
    )
    return watsonx_llm


def initialize_rag():
    global _qa_chain
    print("Initializing RAG Pipeline...")

    # 1. Load documents
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Data file not found at {DATA_FILE}")
        
    loader = TextLoader(DATA_FILE)
    documents = loader.load()

    # 2. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 3. Create Vector Store with Local Embeddings
    # We use all-MiniLM-L6-v2 which is fast and good for general semantic search
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Check if vector store exists
    if not os.path.exists(VECTOR_STORE_DIR):
        print("Creating new vector store...")
        vectorstore = Chroma.from_documents(
            documents=texts, 
            embedding=embedding_function, 
            persist_directory=VECTOR_STORE_DIR
        )
        vectorstore.persist()
    else:
        print("Loading existing vector store...")
        vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_function)

    # 4. Initialize LLM
    llm = get_llm()
    if llm is None:
        print("Skipping full initialization due to missing IBM Cloud credentials.")
        return

    # 5. Create RetrievalQA chain
    prompt_template = """Use the following pieces of context to answer the user's question about Global Tech University college admissions.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Helpful Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    _qa_chain = {
        "llm": llm,
        "retriever": vectorstore.as_retriever(search_kwargs={"k": 3}),
        "prompt": PROMPT
    }
    print("RAG Pipeline initialized successfully.")

def query_agent(question: str) -> dict:
    if _qa_chain is None:
        return {
            "answer": "The RAG pipeline is not initialized because IBM Cloud credentials are not configured. Please set IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID.",
            "sources": []
        }
        
    try:
        # Retrieve context
        docs = _qa_chain["retriever"].invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Build prompt and invoke LLM
        prompt_str = _qa_chain["prompt"].format(context=context, question=question)
        answer = _qa_chain["llm"].invoke(prompt_str)
        
        return {
            "answer": answer.strip(),
            "sources": [doc.page_content for doc in docs]
        }
    except Exception as e:
        return {
            "answer": f"An error occurred while generating the response: {str(e)}",
            "sources": []
        }

if __name__ == "__main__":
    # Test initialization
    initialize_rag()
