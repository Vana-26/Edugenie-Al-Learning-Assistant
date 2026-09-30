# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant for students. It supports:

- Question & Answer
- Simple concept explanations
- Automatic 3-question MCQ quizzes
- Study-note summarization
- Personalized beginner-to-advanced learning paths

## Tech Stack

- Python 3.10+
- FastAPI
- Google Gemini API via the official `google-genai` SDK
- HTML, CSS and JavaScript
- Jinja2
- Uvicorn

## Project Structure

```text
EduGenie/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## Run Locally

### 1. Create a virtual environment

Windows:
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Copy `.env.example` to `.env` and add your key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

Never commit `.env` or your API key to GitHub.

### 4. Start the application

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/qa` | Answer a question |
| POST | `/api/explain` | Explain a topic |
| POST | `/api/quiz` | Generate 3 MCQs |
| POST | `/api/summarize` | Summarize notes |
| POST | `/api/learn/recommendations` | Create a learning path |
| GET | `/health` | Health/configuration check |

Legacy endpoints matching the original project specification are also available: `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`.

## Testing

```bash
pytest
```

## Project Highlights

This implementation follows the original EduGenie concept of a FastAPI backend, HTML/CSS frontend, modular educational features, quiz generation, summarization, and learning recommendations. The Gemini integration uses the current Google GenAI SDK rather than the older SDK pattern.

## Future Enhancements

- User accounts and saved learning history
- Progress dashboard and streaks
- Multilingual learning
- PDF/image-based doubt solving
- Voice interaction
- Teacher/parent dashboards
- LMS integrations
