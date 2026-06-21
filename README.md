# PatentScout 🔍

**AI-Powered Patent Research & Prior-Art Search**

PatentScout is an internal tool designed to help R&D engineers and legal analysts quickly determine if a new technical idea risks infringing on existing patents. You paste a plain-English description of an invention, and our AI pipeline will abstract the concept, search through real patent databases, and generate a comprehensive risk report in real-time.

---

## 🛠️ The Technology Stack (Explained)

If you are new to this project, don't worry! Here is a breakdown of the tools we are using and why:

*   **[Python 3.11+](https://www.python.org/)**: The core language for our backend.
*   **[uv](https://github.com/astral-sh/uv)**: An extremely fast Python package manager (written in Rust). It replaces `pip` and `virtualenv`. We use it because it makes installing dependencies almost instant.
*   **[Agno](https://github.com/agno-ai/agno)** (formerly Phidata): Our AI Agent framework. It provides the "AgentOS" which automatically handles API endpoints, Server-Sent Events (SSE) for streaming text, and AI workflow coordination.
*   **[FastAPI](https://fastapi.tiangolo.com/)**: The web framework powering our backend API. It is incredibly fast and Agno runs on top of it.
*   **[FAISS](https://github.com/facebookresearch/faiss)**: A library developed by Facebook AI for highly efficient similarity search. We use it to quickly search through millions of patent "vector embeddings" (mathematical representations of text).
*   **SQLite**: A lightweight, file-based database. We use it to save user session history and generated reports.
*   **React + [Vite](https://vitejs.dev/)**: Our frontend framework. Vite is a build tool that makes React development lightning fast compared to older tools like Create React App.

---

## 🧠 The AI Multi-Agent Pipeline

The core intelligence of PatentScout is powered by a multi-agent workflow where specialized AI "Agents" pass data to each other in sequence. This prevents hallucinations and enforces a strict legal tone.

1. **Concept Abstractor**: Receives a raw, unstructured technical idea from the user and extracts structured, patent-like "functional claims" and search keywords.
2. **Patent Searcher**: Takes those keywords and queries our local FAISS vector database to retrieve the most similar existing patents.
3. **Infringement Matcher**: Acts as a strict legal analyst. It takes the retrieved patents and the user's abstracted claims, and performs a claim-by-claim structural overlap analysis to generate a risk score (High/Medium/Low).
4. **Report Drafter**: Takes all the raw findings, scores, and context, and synthesizes it into a beautifully formatted, objective Markdown report that streams back to the user interface.

*These are orchestrated inside `workflows/analysis_pipeline.py`, which manages the state hand-offs.*

---

## 📂 Project Structure

Here is where everything lives:

*   `app.py` - The main FastAPI application and AgentOS configuration.
*   `database.py` - Initializes the SQLite database.
*   `docs/prd.md` - The Product Requirements Document (what we are building).
*   `frontend/` - The React user interface.
*   `agents/` - Individual AI agents (e.g., Concept Abstractor, Similarity Analyzer).
*   `workflows/` - Coordinates how agents talk to each other sequentially.
*   `faiss_index/` - Where the local FAISS vector database files are stored.
*   `db/` - Where the SQLite database file (`sessions.db`) is stored.
*   `scripts/` & `tools/` - Standalone tools and functions the AI agents can execute.

---

## 🚀 Development Setup

We have made setting up the environment as painless as possible.

### Prerequisites
1. Install **Python 3.11+**.
2. Install **Node.js**.
3. Install **uv** by opening your terminal and running:
   * **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   * **Mac/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 1-Click Setup (Windows)
Open PowerShell, navigate to the project folder, and run:
```powershell
.\setup_dev.ps1
```
*What this script does:* It creates necessary folders, initializes the Python virtual environment, installs backend dependencies via `uv`, installs frontend dependencies via `npm`, and configures `pre-commit` hooks (which automatically format your code before you save it to Git).

### Manual Setup (If the script fails or you are on Mac/Linux)
**Backend:**
```bash
uv venv
uv pip install -e ".[dev]"
uv run pre-commit install
```
**Frontend:**
```bash
cd frontend
npm install
```

---

## 💻 Running the Application

You will need two separate terminal windows open to run the full application.

### Terminal 1: Backend (FastAPI + Agno)
1. Ensure your `.env` file is created (copy `.env.example` to `.env` and add your `OPENAI_API_KEY`).
2. Activate your virtual environment:
   * **Windows:** `.venv\Scripts\activate`
   * **Mac/Linux:** `source .venv/bin/activate`
3. Start the server:
   ```bash
   uv run uvicorn app:app --reload
   ```
   *The API is now running at http://localhost:8000.*

### Terminal 2: Frontend (React)
1. Navigate into the frontend folder:
   ```bash
   cd frontend
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   *The UI is now running at the local address printed in your terminal (usually http://localhost:5173).*

---

## 🌿 Git & Pull Request Guidelines

To keep our codebase clean and stable, please follow these rules:

1. **Never commit directly to `master` (or `main`)**: `master` should always be in a working, deployable state.
2. **Branch Naming**:
   * Adding a feature? Create a branch named `feature/your-feature-name`.
   * Fixing a bug? Create a branch named `bugfix/your-bug-name`.
3. **Pre-commit Hooks**: We use `pre-commit` to ensure code is formatted correctly. When you type `git commit`, our tools will automatically run and fix minor formatting issues. If it fails, just type `git commit` a second time after the tools fix the files!
4. **Pull Requests (PRs)**: When your code is ready, open a Pull Request against the `master` branch. Ask a teammate to review your code before merging.
