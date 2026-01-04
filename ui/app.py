import streamlit as st
import requests
import matplotlib.pyplot as plt

# ================== CONFIG ==================
API_URL = "https://dsa-tracker-7yfw.onrender.com"

st.set_page_config(page_title="DSA Tracker", layout="wide")
st.title("📘 DSA Tracker Dashboard")

# ================== SAFE API CALL ==================
def safe_get(url, default):
    try:
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        return res.json()
    except Exception:
        return default

def safe_post(url, params=None):
    try:
        res = requests.post(url, params=params, timeout=60)
        res.raise_for_status()
        return res.json()
    except Exception:
        return {"message": "⚠️ Backend waking up, try again"}

# ================== ADD QUESTION ==================
st.subheader("➕ Add Question")

col1, col2, col3 = st.columns(3)

with col1:
    q_no = st.text_input("Question No (e.g. LC-1)")

with col2:
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

with col3:
    patterns = st.multiselect(
        "Patterns",
        ["array", "hashmap", "two-pointers", "sliding-window", "dp", "graph", "tree"]
    )

if st.button("Add Question"):
    if q_no:
        res = safe_post(
            f"{API_URL}/add-question",
            params={"q_no": q_no, "difficulty": difficulty, "patterns": patterns}
        )
        st.success(res.get("message", "Done"))
        st.rerun()
    else:
        st.warning("Enter Question No")

st.divider()

# ================== TODAY TASKS ==================
st.subheader("📅 Today's Tasks")

today_data = safe_get(f"{API_URL}/today", {"tasks": []})
tasks = today_data.get("tasks", [])

if not tasks:
    st.info("🎉 Nothing to do today")
else:
    for q, d, p in tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{q}** ({d}) | Patterns: {', '.join(p) if p else '—'}")
        with col2:
            if st.button(f"Mark Done {q}"):
                res = safe_post(f"{API_URL}/done", params={"q_no": q})
                st.success(res.get("message", "Done"))
                st.rerun()

st.divider()

# ================== CONSISTENCY ==================
st.subheader("🔥 Consistency")

cons = safe_get(
    f"{API_URL}/consistency",
    {"score": 0, "current_streak": 0, "max_streak": 0}
)

c1, c2, c3 = st.columns(3)
c1.metric("Consistency %", f"{cons['score']}%")
c2.metric("Current Streak", cons["current_streak"])
c3.metric("Best Streak", cons["max_streak"])

st.divider()

# ================== MISSED DAYS ==================
st.subheader("❌ Missed Days")

missed = safe_get(f"{API_URL}/missed", {})

if not missed:
    st.success("No missed days 🎉")
else:
    for q, days in missed.items():
        st.write(f"**{q}** → {days}")

st.divider()

# ================== WEAK QUESTIONS ==================
st.subheader("⚠️ Weak Questions")

weak = safe_get(f"{API_URL}/weak", {})

if not weak:
    st.success("No weak questions 🎉")
else:
    for q, cnt in weak.items():
        st.write(f"**{q}** → Missed {cnt} times")

st.divider()

# ================== ANALYTICS ==================
st.subheader("📊 Analytics Overview")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Consistency %", f"{cons['score']}%")
k2.metric("Current Streak", cons["current_streak"])
k3.metric("Weak Questions", len(weak))
k4.metric("Pending Today", len(tasks))

labels = ["Pending Today", "Weak Questions"]
values = [len(tasks), len(weak)]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("Count")
ax.set_title("DSA Tracker Status")

st.pyplot(fig)

# ================== DAILY TREND ==================
st.subheader("📈 Solves Per Day")

daily = safe_get(f"{API_URL}/daily-activity", {})

if daily:
    dates = list(daily.keys())
    counts = list(daily.values())

    fig2, ax2 = plt.subplots()
    ax2.plot(dates, counts, marker="o")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Solved Count")
    ax2.set_title("Daily Solves Trend")

    st.pyplot(fig2)
else:
    st.info("No activity data yet")

# ================== PATTERN ANALYTICS ==================
st.subheader("🧠 Pattern Weakness Analysis")

pattern_stats = safe_get(f"{API_URL}/patterns", {})

if not pattern_stats:
    st.success("No pattern data yet 🎉")
else:
    labels = list(pattern_stats.keys())
    values = list(pattern_stats.values())

    fig3, ax3 = plt.subplots()
    ax3.bar(labels, values)
    ax3.set_ylabel("Miss Count")
    ax3.set_title("Weak DSA Patterns")

    st.pyplot(fig3)
