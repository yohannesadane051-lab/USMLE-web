import json
import os
import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="USMLE Question Bank",
    layout="centered"
)

# ---------------- LOAD QUESTIONS ----------------
@st.cache_data
def load_questions():
    json_path = "questions.json"
    if not os.path.exists(json_path):
        st.error("❌ questions.json not found")
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# ---------------- SESSION STATE ----------------
if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None

# ---------------- HEADER ----------------
st.title("🩺 USMLE Question Bank")

if questions:
    st.caption(f"Loaded {len(questions)} questions")
else:
    st.stop()

# ---------------- QUIZ LOGIC ----------------
if st.session_state.idx < len(questions):

    q = questions[st.session_state.idx]

    st.markdown(
        f"### Question {st.session_state.idx + 1} of {len(questions)}"
    )
    st.progress((st.session_state.idx) / len(questions))

    st.markdown(
        f"**{q.get('subject', 'General Medicine')}** — {q.get('topic', 'General')}"
    )

    st.markdown(q.get("question", ""))

    options = q.get("options", [])
    correct_answer = q.get("answer", "A")

    # ---------------- ANSWER SELECTION ----------------
    for i, opt in enumerate(options):
        letter = chr(65 + i)
        label = f"{letter}. {opt}"

        if st.button(
            label,
            key=f"opt_{i}",
            disabled=st.session_state.answered
        ):
            st.session_state.selected = letter
            st.session_state.answered = True

            if letter == correct_answer:
                st.session_state.score += 1

    # ---------------- EXPLANATION ----------------
    if st.session_state.answered:
        if st.session_state.selected == correct_answer:
            st.success("✅ Correct!")
        else:
            st.error(
                f"❌ Incorrect — Correct answer: **{correct_answer}**"
            )

        st.markdown("#### Explanation")
        st.markdown(q.get("explanation", "No explanation available."))

        if "educational_objective" in q:
            st.markdown(
                f"🎯 **Key Point:** {q['educational_objective']}"
            )

        # ---------------- NEXT BUTTON ----------------
        if st.button("Next Question ▶️"):
            st.session_state.idx += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()

else:
    # ---------------- QUIZ COMPLETE ----------------
    percentage = (st.session_state.score / len(questions)) * 100

    st.balloons()
    st.markdown("## 🎉 Quiz Complete!")
    st.markdown(
        f"### Final Score: **{st.session_state.score}/{len(questions)}** ({percentage:.1f}%)"
    )

    if st.button("Restart Quiz 🔁"):
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()
