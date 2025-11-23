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

