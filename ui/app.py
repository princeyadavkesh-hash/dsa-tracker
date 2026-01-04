import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DSA Tracker", layout="wide")

st.title("📘 DSA Tracker Dashboard")

# ------------------ ADD QUESTION ------------------
st.subheader("➕ Add Question")

col1, col2, col3 = st.columns(3)

with col1:
    q_no = st.text_input("Question No (e.g. LC-1)")

with col2:
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

with col3:
    if st.button("Add"):
        if q_no:
            res = requests.post(
                f"{API_URL}/add-question",
                params={"q_no": q_no, "difficulty": difficulty}
            )
            st.success(res.json()["message"])
        else:
            st.warning("Enter Question No")

st.divider()

# ------------------ TODAY TASKS ------------------
st.subheader("📅 Today's Tasks")

tasks = requests.get(f"{API_URL}/today").json()["tasks"]

if not tasks:
    st.info("🎉 Nothing to do today")
else:
    for q, d in tasks:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{q}** ({d})")
        with col2:
            if st.button(f"Mark Done {q}"):
                res = requests.post(f"{API_URL}/done", params={"q_no": q})
                st.success(res.json()["message"])
                st.rerun()


st.divider()

# ------------------ CONSISTENCY ------------------
st.subheader("🔥 Consistency")

cons = requests.get(f"{API_URL}/consistency").json()

c1, c2, c3 = st.columns(3)
c1.metric("Consistency %", f"{cons['score']}%")
c2.metric("Current Streak", cons["current_streak"])
c3.metric("Best Streak", cons["max_streak"])

st.divider()

# ------------------ MISSED DAYS ------------------
st.subheader("❌ Missed Days")

missed = requests.get(f"{API_URL}/missed").json()

if not missed:
    st.success("No missed days 🎉")
else:
    for q, days in missed.items():
        st.write(f"**{q}** → {days}")

st.divider()

# ------------------ WEAK QUESTIONS ------------------
st.subheader("⚠️ Weak Questions")

weak = requests.get(f"{API_URL}/weak").json()

if not weak:
    st.success("No weak questions 🎉")
else:
    for q, cnt in weak.items():
        st.write(f"**{q}** → Missed {cnt} times")



import pandas as pd
import matplotlib.pyplot as plt

st.divider()
st.subheader("📊 Analytics Overview")

# --------- FETCH DATA ----------
cons = requests.get(f"{API_URL}/consistency").json()
today_tasks = requests.get(f"{API_URL}/today").json()["tasks"]
weak = requests.get(f"{API_URL}/weak").json()
missed = requests.get(f"{API_URL}/missed").json()

# --------- KPIs ----------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Consistency %", f"{cons['score']}%")
k2.metric("Current Streak", cons["current_streak"])
k3.metric("Weak Questions", len(weak))
k4.metric("Pending Today", len(today_tasks))

# --------- BAR CHART ----------
st.subheader("📌 Status Distribution")

labels = ["Pending Today", "Weak Questions"]
values = [len(today_tasks), len(weak)]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("Count")
ax.set_title("DSA Tracker Status")

st.pyplot(fig)

st.subheader("📈 Activity Trends")

# --------- LOAD RAW DATA ----------
data = requests.get(f"{API_URL}/missed").json()
all_tasks = requests.get(f"{API_URL}/today").json()["tasks"]

# --------- SOLVES PER DAY (APPROX) ----------
# We count total solves from weak + today as proxy (v1 logic)
solves_today = len(all_tasks)

trend_labels = ["Today"]
trend_values = [solves_today]

fig2, ax2 = plt.subplots()
ax2.plot(trend_labels, trend_values, marker="o")
ax2.set_ylabel("Solves")
ax2.set_title("Solves Trend (Daily)")

st.pyplot(fig2)
