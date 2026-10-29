# ResumePilot

ResumePilot is a local-first resume analyzer for college placement cells. It accepts PDF, DOCX, or pasted text, produces transparent advisory analysis, and stores analysis history in SQLite.

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `backend/.env.example` to `backend/.env` for local configuration. The included analyzer is a clearly labeled deterministic demo provider; connect an approved LLM adapter in `app/analyzer.py` before enabling provider-backed analysis.

### Frontend

Node.js 18+ is required.

```powershell
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:8000`.

## Privacy

Resume text is used only to create the requested report. Analysis records are local SQLite rows and can be deleted from Analysis History. Uploaded files are processed in memory and are not retained. AI advice is advisory and must not be used to rank students using protected characteristics.
