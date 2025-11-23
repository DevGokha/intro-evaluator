let radarChart = null;

function runEvaluation() {
    const transcript = document.getElementById("transcript").value.trim();
    const duration = document.getElementById("duration").value || null;
    const scoreSummary = document.getElementById("scoreSummary");
    const detailPane = document.getElementById("detailPane");
    const radarContainer = document.getElementById("radarContainer");

    if (transcript.length < 10) {
        scoreSummary.innerHTML = "<p class='loading'>❗ Please enter a longer transcript (at least one or two sentences).</p>";
        detailPane.innerHTML = "<p style='color:#fca5a5;'>Transcript too short to evaluate meaningfully.</p>";
        radarContainer.style.display = "none";
        return;
    }

    scoreSummary.innerHTML = "<div class='loading'>⏳ Evaluating transcript…</div>";
    detailPane.innerHTML = "";

    fetch("/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            transcript: transcript,
            duration_seconds: duration
        })
    })
    .then(response => response.json())
    .then(data => {
        renderDashboard(data);
    })
    .catch(err => {
        scoreSummary.innerHTML = "<p class='loading'>⚠️ Error: " + err + "</p>";
        radarContainer.style.display = "none";
    });
}

function renderDashboard(data) {
    const scoreSummary = document.getElementById("scoreSummary");
    const detailPane = document.getElementById("detailPane");
    const radarContainer = document.getElementById("radarContainer");

    const overall = data.overall_score;
    const criteria = data.criteria_scores;

    const scoreColorClass =
        overall >= 85 ? "tag-green" :
        overall >= 70 ? "tag-yellow" : "tag-red";

    const labelText =
        overall >= 90 ? "Excellent" :
        overall >= 80 ? "Very Good" :
        overall >= 70 ? "Good" :
        overall >= 60 ? "Needs Improvement" : "Weak";

    // ---------- Score Summary + Criteria Cards ----------
    let criteriaCardsHTML = "";
    const radarLabels = [];
    const radarData = [];

    for (const [name, info] of Object.entries(criteria)) {
        const score01 = info.score ?? 0;
        const score100 = Math.round(score01 * 100);
        const weight = info.weight ?? 0;

        radarLabels.push(name);
        radarData.push(score100);

        const barClass =
            score100 >= 85 ? "bar-green" :
            score100 >= 70 ? "bar-yellow" : "bar-red";

        criteriaCardsHTML += `
            <div class="criterion-card">
                <div class="criterion-title">${name}</div>
                <div class="criterion-score">${score100}</div>
                <div class="criterion-weight">Weight: ${(weight * 100).toFixed(0)}%</div>
                <div class="bar">
                    <div class="bar-fill ${barClass}" style="width: ${score100}%;"></div>
                </div>
            </div>
        `;
    }

    scoreSummary.innerHTML = `
        <p class="score-label">Overall Score</p>
        <p class="overall-score">${overall}</p>
        <span class="score-tag ${scoreColorClass}">${labelText}</span>

        <div class="metrics-row">
            <div class="metric-pill">Words: ${data.word_count}</div>
            <div class="metric-pill">Sentences: ${data.sentence_count}</div>
        </div>

        <h3 style="margin-top: 18px; font-size:16px;">Criteria Scores</h3>
        <div class="criteria-grid">
            ${criteriaCardsHTML}
        </div>
    `;

    // ---------- Details Pane ----------
    let detailHTML = "";

    for (const [name, info] of Object.entries(criteria)) {
        const cloned = { ...info };
        delete cloned.weight;
        const score100 = Math.round((info.score ?? 0) * 100);

        detailHTML += `
            <div style="margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #111827;">
                <div style="font-weight:600; margin-bottom:4px;">${name} (${score100})</div>
                <pre>${JSON.stringify(cloned, null, 2)}</pre>
            </div>
        `;
    }

    detailPane.innerHTML = detailHTML || "<p style='color:#9ca3af;'>No details available.</p>";

    // ---------- Radar Chart ----------
    radarContainer.style.display = "block";
    const ctx = document.getElementById("radarChart").getContext("2d");

    if (radarChart) {
        radarChart.destroy();
    }

    radarChart = new Chart(ctx, {
        type: "radar",
        data: {
            labels: radarLabels,
            datasets: [{
                label: "Score",
                data: radarData,
                borderWidth: 2,
                pointRadius: 3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: "#e5e7eb" } }
            },
            scales: {
                r: {
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { color: "#9ca3af", stepSize: 20 },
                    grid: { color: "#1f2937" },
                    angleLines: { color: "#1f2937" },
                    pointLabels: { color: "#e5e7eb" }
                }
            }
        }
    });
}
