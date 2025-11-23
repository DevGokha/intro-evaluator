# Student Introduction Evaluation Tool

A standalone rubric-based scoring system for evaluating spoken or written student introductions.  
This project evaluates a transcript using a configurable Excel rubric and returns a weighted score, criterion-level breakdowns, grammar/clarity metrics, speech-rate estimates, and diagnostic feedback.

This repository is independent and not related to any other project.

Live/demo: self-hosted FastAPI backend + simple frontend

## What it does

- Accepts a transcript (text) and optional duration (seconds)
- Loads a rubric from an Excel file (dynamic, weighted criteria)
- Computes per-criterion scores and a weighted overall score (0–100)
- Provides:
  - Overall score
  - Criterion-wise scores and notes
  - Grammar/spelling hints
  - Filler word counts
  - Word/sentence counts and estimated WPM
  - Sentiment/engagement estimate
  - Structured JSON output for UI or API consumers

## Key features

- Excel-based dynamic rubric ingestion
- Rule-based checks (greeting, name, goals, closing)
- Keyword/pattern detection and simple flow analysis
- Grammar estimation via lightweight spell-checking
- Filler-word detection and counts
- Sentiment analysis (VADER)
- Approximate speech-rate estimation using duration (WPM)
- Simple web UI and OpenAPI/Swagger for testing

## Quick architecture

index.html (UI) → POST /score → FastAPI backend
- rubric_loader.py — load & normalize rubric
- scoring.py — scoring rules, grammar/filler/sentiment modules
- main.py — API endpoints and orchestration
- models.py — Pydantic request/response schemas

Returns JSON scoring response consumable by UI or other services.

## Folder structure

intro-evaluator/
├── backend/
│   ├── main.py
│   ├── scoring.py
│   ├── rubric_loader.py
│   ├── models.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── script.js
├── rubric/
│   └── case-study-rubric.xlsx
└── sample/
    └── sample-transcripts.txt

## API

POST /score
- Request:
  {
    "transcript": "Hello everyone, my name is ...",
    "duration_seconds": 52    // optional
  }

- Response:
  {
    "overall_score": 92.1,
    "criteria_scores": { ... },
    "word_count": 134,
    "sentence_count": 11,
    "filler_count": 3,
    "wpm_estimate": 154,
    "sentiment": { "compound": 0.71, "label": "positive" }
  }

## How to run locally

1. Create and activate a Python virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. From the backend directory:
   uvicorn main:app --reload
4. Open the UI at:
   http://127.0.0.1:8000
5. Use Swagger docs:
   http://127.0.0.1:8000/docs

Notes:
- Place your rubric Excel at `rubric/case-study-rubric.xlsx` or change the path in `rubric_loader.py`.
- If `duration_seconds` is omitted, WPM-based scoring is skipped or approximated.

## Tech stack

- Python 3.x, FastAPI, Uvicorn
- pandas (Excel parsing)
- pyspellchecker (light grammar hints) or similar
- NLTK VADER for sentiment
- Regex-based NLP for filler/keyword detection
- Jinja2 + plain JS frontend

## Rubric & scoring

- Rubric stored in Excel with fields: criterion, max_score, weight (weights are normalized)
- Each scoring function returns a score and notes; overall score = Σ(score × normalized_weight)

## Limitations & future work

- Replace spellchecker heuristics with LanguageTool or a grammar API
- Add speech-to-text pipeline to accept audio inputs
- Use semantic embeddings for deeper content quality assessment
- Build a teacher dashboard and batch evaluation mode
- Add unit tests and CI for scoring functions

## Author

Dev Gokha  
AI/ML Developer

