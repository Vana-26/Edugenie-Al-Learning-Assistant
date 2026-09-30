import json
import os
import re
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

try:
    from google import genai
except ImportError:
    genai = None

load_dotenv()

APP_NAME = "EduGenie"
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title=APP_NAME, version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = genai.Client(api_key=API_KEY) if (genai and API_KEY) else None

SYSTEM = (
    "You are EduGenie, a friendly educational assistant. "
    "Give accurate, concise, student-friendly answers. Explain difficult ideas simply. "
    "Do not invent sources or facts. If uncertain, say so."
)


def call_gemini(prompt: str) -> str:
    if client is None:
        return (
            "EduGenie demo mode: add GEMINI_API_KEY to the .env file to enable "
            "AI-generated responses. Your request was received successfully."
        )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"system_instruction": SYSTEM, "temperature": 0.3},
    )
    text = getattr(response, "text", None)
    return text.strip() if text else "No response was generated. Please try again."


def clean_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(text: str):
    prompt = f"""Create exactly 3 multiple-choice questions from this educational passage.
Return ONLY valid JSON in this shape:
{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":"A"}}]}}
The answer field must exactly match one option. Keep questions suitable for students.

PASSAGE:
{text}"""
    raw = call_gemini(prompt)
    try:
        data = json.loads(clean_json(raw))
        questions = data.get("questions", [])
        if not isinstance(questions, list) or len(questions) != 3:
            raise ValueError("Expected exactly 3 questions")
        return {"questions": questions}
    except Exception:
        return {"error": "Quiz generation returned an invalid format. Please try again."}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": APP_NAME})


@app.get("/health")
async def health():
    return {"status": "ok", "gemini_configured": client is not None, "model": MODEL}


@app.post("/api/explain")
async def explain(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text:
        return JSONResponse({"error": "Please enter a topic."}, status_code=400)
    return {"result": call_gemini(f"Explain this topic in simple language with a short example:\n{text}")}


@app.post("/api/qa")
async def qa(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text:
        return JSONResponse({"error": "Please enter a question."}, status_code=400)
    return {"result": call_gemini(f"Answer this student question clearly and directly:\n{text}")}


@app.post("/api/summarize")
async def summarize(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text:
        return JSONResponse({"error": "Please enter text to summarize."}, status_code=400)
    return {"result": call_gemini(f"Summarize the following educational text into clear key points. Preserve important meaning:\n{text}")}


@app.post("/api/learn/recommendations")
async def recommendations(payload: dict):
    topic = str(payload.get("text", "")).strip()
    if not topic:
        return JSONResponse({"error": "Please enter a topic."}, status_code=400)
    prompt = f"""Create a personalized learning path for: {topic}
Organize it as Beginner -> Intermediate -> Advanced.
For each level give topics, a simple goal, and suggested resource types (video/article/book/docs).
Keep it practical for a student."""
    return {"result": call_gemini(prompt)}


@app.post("/api/quiz")
async def quiz(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text:
        return JSONResponse({"error": "Please enter a topic or passage."}, status_code=400)
    return generate_quiz(text)


# Backward-compatible endpoints matching the project document.
@app.post("/qa")
async def qa_legacy(payload: dict):
    return await qa(payload)

@app.post("/explain")
async def explain_legacy(payload: dict):
    return await explain(payload)

@app.post("/summarize")
async def summarize_legacy(payload: dict):
    return await summarize(payload)

@app.post("/learn/recommendations")
async def recommendations_legacy(payload: dict):
    return await recommendations(payload)

@app.post("/quiz")
async def quiz_legacy(payload: dict):
    return await quiz(payload)
