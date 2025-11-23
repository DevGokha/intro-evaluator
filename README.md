# 🎙️ Intro Evaluator – Student Introduction Scoring Tool  
A rubric-driven evaluation system that scores a student's spoken introduction using NLP, sentiment analysis, filler-word detection, grammar scoring, and rubric weights extracted directly from Excel.

This project was built as part of the **NirmaanAI Case Study**.  
It demonstrates **product thinking**, **clean architecture**, and **end-to-end workflow design**.

---

## 🚀 Features

### ✔ Rubric-Based Scoring (from Excel)
The tool reads the official rubric (`Case study for interns.xlsx`) and extracts:
- Criteria  
- Metrics  
- Weightages  
- Normalized weights  

No hardcoding — fully dynamic.

### ✔ NLP-Based Evaluation
Each transcript is analyzed for:
- **Content & Structure**
- **Speech Rate**
- **Grammar Score** (Spellchecker)
- **Clarity** (Filler-word rate)
- **Engagement** (Sentiment score)

### ✔ Clean API + Fast Dashboard
- FastAPI backend (`/score`)
- Modern UI with:
  - Radar chart  
  - Weighted scoring breakdown  
  - Color-coded progress bars  
  - JSON detail panel  

### ✔ Easy Local Deployment
- Virtual environment  
- `requirements.txt`  
- Clean instructions (PDF included)  

---

## 📄 Problem Statement

Build a tool that uses the provided **rubric Excel file** and **sample transcript**  
to evaluate a student’s introduction, return structured scores,  
and visualize them in a user-friendly dashboard.

This case study is intentionally open-ended — the solution focuses on structured product design rather than raw coding.

---

## 🧠 Scoring Logic Overview

Each transcript passes through these steps:

### 1️⃣ **Preprocessing**
- Clean text  
- Tokenization  
- Sentence extraction  
- Word count  

### 2️⃣ **Criteria Evaluation**

| Criterion | Method | Output |
|----------|--------|---------|
| Content & Structure | Rule-based pattern detection | 0–1 |
| Speech Rate | WPM calculation | 0–1 |
| Grammar | Spellchecker errors per 100 words | 0–1 |
| Clarity | Filler-word frequency | 0–1 |
| Engagement | Sentiment score (VADER) | 0–1 |

### 3️⃣ **Weighted Scoring**

The Excel gives weightages:

Content & Structure – 40%
Speech Rate – 10%
Grammar – 20%
Clarity – 15%
Engagement – 15%


Final score = Σ (score_i × weight_i) × 100

---

## 🏗️ Project Architecture


---

## 🖼️ Screenshots

### Dashboard UI  
  
[![Dashboard Screenshot](PATH_TO_YOUR_SCREENSHOT_1)](https://drive.google.com/file/d/1S10KHKZnw1QA99sN0xIwxYHsfcVOCWG6/view?usp=sharing)

### Detailed Breakdown  
[![Detailed View](PATH_TO_YOUR_SCREENSHOT_2)](https://drive.google.com/file/d/1_Rs-zVldc6jp7atek_aZASFlff41ESf5/view?usp=sharing)

### API Documentation  
[![Swagger](PATH_TO_YOUR_SCREENSHOT_3)](https://drive.google.com/file/d/1kRE9r3mgGaoCVpxuZQnUENJY_GR5cPJC/view?usp=sharing)

---

## 🔧 Installation & Local Run

### 1. Clone Repo
```bash
git clone https://github.com/DevGokha/intro-evaluator.git
cd intro-evaluator

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run API Server
cd backend
uvicorn main:app --reload

5. Open in Browser

Dashboard → http://127.0.0.1:8000

API Docs → http://127.0.0.1:8000/docs

📡 API Documentation
POST /score

Request:

{
  "transcript": "Hello everyone, my name is...",
  "duration_seconds": 50
}


Response:

{
  "overall_score": 92.1,
  "criteria_scores": {
    "Content & Structure": { "score": 0.95, "weight": 0.4 },
    "Speech Rate": { "score": 0.8, "wpm": 154.2, "weight": 0.1 },
    "Grammar": { "score": 0.8, "errors_per_100": 1.49, "weight": 0.2 },
    ...
  }
}

🎥 Demo Video

https://drive.google.com/drive/folders/ADD_YOUR_LINK

📝 Case Study Reflection

  This solution was developed with a focus on:
  
  Structured product thinking
  
  Clear evaluation logic
  
  Clean API architecture
  
  User-friendly dashboard
  
  Interpretable scoring

Even though the case study is intentionally open-ended, the system is fully functional and extensible.

👤 Author

Dev Gokha
Email: devgokha434@gmail.com
GitHub: https://github.com/DevGokha
