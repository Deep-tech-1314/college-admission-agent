# 🎓 College Admission Agent (RAG-Powered)

Welcome to the **College Admission Agent**, an intelligent, Retrieval-Augmented Generation (RAG) assistant designed to streamline the student admission process. 

Powered by **IBM watsonx.ai (Granite)**, this assistant retrieves official admission policies, eligibility criteria, and fee structures from an internal vector database and answers student queries accurately and transparently.

![App Preview](frontend/src/assets/react.svg) *(Built with React, Vite, FastAPI, and LangChain)*

---

## ✨ Features

- **🧠 Intelligent RAG Pipeline:** Connects directly to IBM Granite (`ibm/granite-8b-code-instruct`) to generate accurate, context-aware answers.
- **📚 Local Vector Store:** Uses ChromaDB and HuggingFace Embeddings (`all-MiniLM-L6-v2`) to perform semantic search over college documents.
- **🎨 Glassmorphic UI:** A stunning, fully responsive React frontend built with Vite and vanilla CSS.
- **🤖 IBM Orchestrate Ready:** Includes a pre-configured `openapi.yaml` to instantly import the RAG skill into IBM watsonx Orchestrate as a Custom Skill.

---

## 🛠️ Tech Stack

- **Frontend:** React, Vite, CSS (Glassmorphism & Light Theme)
- **Backend:** Python, FastAPI, Uvicorn
- **AI/LLM:** LangChain, ChromaDB, IBM watsonx.ai (Granite)

---

## 🚀 Quick Start

### 1. Configure the Backend
Navigate to the `backend/` folder and create a `.env` file based on `.env.example`:
```env
IBM_CLOUD_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://au-syd.ml.cloud.ibm.com
```

### 2. Run the Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*(The FastAPI server will run on `http://localhost:8000`)*

### 3. Run the Frontend
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
*(The React UI will run on `http://localhost:5173`)*

---

## 🤝 IBM watsonx Orchestrate Integration

To use this agent inside IBM Orchestrate:
1. Expose your backend via a public tunnel (e.g., `localtunnel` or deploy to IBM Cloud Code Engine).
2. Update the `url` in the `openapi.yaml` file.
3. In the Orchestrate Dashboard, go to **Build** > **Add Skill** > **From OpenAPI**.
4. Upload `openapi.yaml` and attach the tool to your Agent!

---

*Developed by Deep Dhamecha as a smart solution for higher education administration.*
