from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


from models import ScoreRequest, ScoreResponse
from rubric_loader import load_rubric
from scoring import (
    preprocess,
    content_structure_score,
    speech_rate_score,
    grammar_score,
    filler_word_score,
    engagement_score,
)

app = FastAPI(title="Student Introduction Evaluator")

templates = Jinja2Templates(directory="templates")

# ⭐ ADD THIS LINE BELOW
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------- Load Rubric ----------
RUBRIC_PATH = r"F:\Assignment1\intro-evaluator\rubric\Case study for interns.xlsx"
rubric_df = load_rubric(RUBRIC_PATH)


# ---------- Home Page ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------- Score API ----------
@app.post("/score", response_model=ScoreResponse)
def score_transcript(req: ScoreRequest):

    pp = preprocess(req.transcript)

    results = {}

    for _, row in rubric_df.iterrows():
        crit_name = row["criteria"]
        metric = row["metric"]
        weight = row["weight"]

        if "Salutation" in metric or "Content" in crit_name:
            s = content_structure_score(pp)
            results["Content & Structure"] = {"score": s, "weight": weight}

        elif "Speech rate" in metric:
            speech = speech_rate_score(pp, req.duration_seconds)
            speech["weight"] = weight
            results["Speech Rate"] = speech

        elif "Grammar errors" in metric:
            g = grammar_score(pp)
            g["weight"] = weight
            results["Language & Grammar"] = g

        elif "Filler Word" in metric:
            f = filler_word_score(pp)
            f["weight"] = weight
            results["Clarity"] = f

        elif "Sentiment" in metric or "positivity" in metric:
            e = engagement_score(pp)
            e["weight"] = weight
            results["Engagement"] = e

    overall = sum(info["score"] * info["weight"] for info in results.values())
    overall_score = round(overall * 100, 2)

    return ScoreResponse(
        overall_score=overall_score,
        criteria_scores=results,
        word_count=pp.word_count,
        sentence_count=pp.sentence_count,
    )
