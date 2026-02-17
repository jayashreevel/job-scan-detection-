from flask import Flask, request, render_template
import sqlite3, pickle
from analyzer import check_keywords, domain_age_check
from search import google_search

app = Flask(__name__, template_folder="templates")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("reports.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    job_description TEXT,
    job_url TEXT,
    result TEXT,
    risk_score INTEGER
)
""")
conn.commit()

# ---------------- LOAD ML MODEL ----------------
model = pickle.load(open("job_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def ml_prediction(text):
    vec = vectorizer.transform([text])
    return model.predict_proba(vec)[0][1]

def suspicious_email(text):
    for mail in ["@gmail.com", "@yahoo.com", "@outlook.com"]:
        if mail in text.lower():
            return True
    return False

# ---------------- HOME ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reason = ""
    links = []

    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        url = request.form["job_url"]

        text = f"{title} {desc} {url}"

        score, matched = check_keywords(text)
        domain_risk = domain_age_check(url)
        email_risk = suspicious_email(text)
        ml_prob = ml_prediction(text)

        if score >= 7 or ml_prob > 0.75:
            result = "❌ FAKE JOB"
            reason = f"High risk detected ({int(ml_prob*100)}%)"
        elif domain_risk or email_risk:
            result = "⚠ HIGH RISK JOB"
            reason = "Suspicious domain or email detected"
        else:
            result = "✅ LOW RISK JOB"
            reason = "No scam indicators found"

        links = google_search(text)

        cursor.execute(
            "INSERT INTO reports (job_title, job_description, job_url, result, risk_score) VALUES (?, ?, ?, ?, ?)",
            (title, desc, url, result, score)
        )
        conn.commit()

    return render_template("index.html", result=result, reason=reason, links=links)

# ---------------- REPORTS ROUTE (DATABASE VIEW) ----------------
@app.route("/reports")
def view_reports():
    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template("reports.html", reports=data)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
