🎤 Student Introduction Evaluation Tool

A rubric-based scoring system for evaluating spoken/written introductions

This tool evaluates a student’s introduction transcript using a structured rubric and returns:

Overall score (0–100)

Criterion-wise score

Grammar/Clarity metrics

Speech rate

Sentiment/engagement

Content & structure quality

It is designed as part of the Nirmaan AI Case Study to demonstrate product thinking, technical execution, and tool-building ability.

🚀 1. Problem Understanding

The goal is to build a tool that:

✔ Accepts a transcript (text input)
✔ Evaluates it using a rubric provided in an Excel file
✔ Produces a weighted score
✔ Provides detailed feedback
✔ Can be tested through UI or API
✔ Is designed with clean, extensible architecture

The problem is open-ended, so the focus is on thought process, workflow design, and tool choice, not just coding.

🧠 2. Product Approach

To solve the problem, I used a hybrid approach:

Rule-Based Evaluation

Keyword and pattern detection

Greeting / name / family / hobbies / goals

Simple flow structure (intro → content → closing)

NLP-Based Evaluation

Sentiment analysis (VADER)

Spelling-based grammar estimation

Filler word detection

Timing-Based Evaluation

Approximate speech rate (WPM) using duration

Weighted Scoring

Rubric weights were normalized and used to compute:

overall_score = Σ (criterion_score × weight)


This ensures consistency with the rubric.

📊 3. System Architecture
                   ┌────────────────┐
                   │   index.html   │
                   │ (Simple UI)    │
                   └───────▲────────┘
                           │  POST /score
                           ▼
┌───────────────────────────────────────────────────────────┐
│                         FastAPI                           │
│                                                           │
│     ┌─────────────┐      ┌──────────────────────────┐     │
│     │ rubric_loader│ ---> │ scoring.py               │     │
│     └─────────────┘      │ (content, grammar,       │     │
│                           │  filler, sentiment…)     │     │
│                                                           │
└───────────────────────────────────────────────────────────┘
                           │
                           ▼
                   JSON Score Output

📁 4. Folder Structure
intro-evaluator/
│
├── backend/
│   ├── main.py
│   ├── scoring.py
│   ├── rubric_loader.py
│   ├── models.py
│   ├── templates/
│   │      └── index.html
│   ├── static/
│          └── script.js
│
├── rubric/
│     └── Case study for interns.xlsx
│
└── sample/
      └── Sample text for case study.txt

🛠 5. Tech Stack
Backend

FastAPI

Python 3

Pandas (Excel parsing)

SpellChecker (light grammar checking)

VADER Sentiment Analysis

Regex-based NLP processing

Frontend

HTML + JS (simple UI)

Jinja2 template rendering

Package installation
pip install -r requirements.txt

🧪 6. How to Run Locally
1️⃣ Navigate to backend folder:
cd backend

2️⃣ Start the FastAPI server:
uvicorn main:app --reload

3️⃣ Open the frontend:

👉 http://127.0.0.1:8000

4️⃣ Test the scoring using:

UI (paste transcript)

Swagger API: http://127.0.0.1:8000/docs

📝 7. API Usage
POST /score
Example Request:
{
  "transcript": "Hello everyone, my name is ...",
  "duration_seconds": 52
}

Example Response:
{
  "overall_score": 92.1,
  "criteria_scores": {
    "Content & Structure": {...},
    "Speech Rate": {...},
    "Language & Grammar": {...},
    "Clarity": {...},
    "Engagement": {...}
  },
  "word_count": 134,
  "sentence_count": 11
}

📌 8. Key Features Implemented
✔ Excel-based dynamic rubric loading
✔ Weighted score computation
✔ Grammar estimation using SpellChecker
✔ Filler word detection
✔ Sentiment analysis
✔ Simple flow analysis
✔ Web UI for easy testing
✔ API for integration
🌱 9. Future Improvements

Real grammar evaluation using LanguageTool (Java required)

Speech-to-text integration (for audio input)

Advanced semantic analysis using embeddings

Visualization dashboard (radar chart for scoring)

Multi-language support

Teacher/admin dashboard

🏁 10. Conclusion

This project demonstrates:

End-to-end product solution

Clean modular architecture

Practical NLP application

Thoughtful rubric interpretation

Clear UI + API usability