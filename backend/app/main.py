from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .analyzer import analyze
from .config import settings
from .database import delete_analysis, get_analysis, get_roles, init_db, list_analyses, save_analysis
from .resume_parser import extract_text
from .schemas import AnalyzeRequest, JobMatchRequest

app = FastAPI(title="ResumePilot API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.post("/api/analyze")
def analyze_resume(request: AnalyzeRequest):
    report = analyze(request.text, request.role, demo=True)
    analysis_id = save_analysis(request.role, request.filename, report["mode"], report)
    return {"id": analysis_id, "role": request.role, "report": report}


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}:
        raise HTTPException(415, "Upload a PDF or DOCX file.")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds the {settings.max_upload_mb} MB limit.")
    try:
        text = extract_text(content, file.filename or "")
    except ValueError as error:
        raise HTTPException(415, str(error)) from error
    if len(text) < 30:
        raise HTTPException(422, "The document did not contain enough readable text.")
    return {"filename": file.filename, "text": text}


@app.get("/api/job-roles")
def job_roles():
    return get_roles()


@app.post("/api/job-match")
def job_match(request: JobMatchRequest):
    return analyze(request.text, request.role, demo=True)["selected_role"]


@app.get("/api/analyses")
def analyses():
    return list_analyses()


@app.get("/api/analyses/{analysis_id}")
def analysis(analysis_id: int):
    result = get_analysis(analysis_id)
    if result is None:
        raise HTTPException(404, "Analysis not found.")
    return result


@app.delete("/api/analyses/{analysis_id}", status_code=204)
def remove_analysis(analysis_id: int):
    if not delete_analysis(analysis_id):
        raise HTTPException(404, "Analysis not found.")
