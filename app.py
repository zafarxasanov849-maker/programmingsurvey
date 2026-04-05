import streamlit as st
from datetime import datetime
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Academic Skill Audit Survey",
    page_icon="📊",
    layout="centered"
)

# ---------------- DATA ----------------
questions = [
    # Section A
    {
        "section": "Section A: Skill Audit Frequency",
        "q": "Q1. How often do you evaluate your own academic skills and abilities?",
        "opts": [
            ("Every week — I have a fixed habit of doing this", 0),
            ("Once or twice a month", 1),
            ("Only before exams or important deadlines", 2),
            ("Rarely — maybe once a semester", 3),
            ("I have never really done this", 4)
        ]
    },
    {
        "q": "Q2. When you notice you are struggling with a subject, how quickly do you identify which specific skill is the problem?",
        "opts": [
            ("Very quickly — I can usually pinpoint it straight away", 0),
            ("Within a few days", 1),
            ("It takes me a week or two to figure it out", 2),
            ("I notice something is wrong but rarely identify the exact skill", 3),
            ("I usually do not figure out what the problem is", 4)
        ]
    },
    {
        "q": "Q3. How honestly do you assess your own weaknesses when reviewing your academic skills?",
        "opts": [
            ("Very honestly — I do not avoid uncomfortable truths", 0),
            ("Mostly honest, though I sometimes overlook things", 1),
            ("I try to be honest but tend to be too easy on myself", 2),
            ("I usually focus only on my strengths", 3),
            ("I do not really assess my weaknesses at all", 4)
        ]
    },
    {
        "q": "Q4. Do you keep any written record of your academic strengths and areas for improvement?",
        "opts": [
            ("Yes — I maintain a regular written record or journal", 0),
            ("Sometimes — I write things down after major assessments", 1),
            ("Rarely — I occasionally make mental notes but not written ones", 2),
            ("No — but I think about it occasionally", 3),
            ("No — I have never tracked this kind of thing", 4)
        ]
    },
    {
        "q": "Q5. How aware are you of the specific academic skills required for your university courses?",
        "opts": [
            ("Very aware — I know exactly what skills each course demands", 0),
            ("Mostly aware — I have a good general idea", 1),
            ("Somewhat aware — I know the obvious ones but miss some details", 2),
            ("Not very aware — I mostly just follow the course content", 3),
            ("Not aware at all — I have not thought about this", 4)
        ]
    },
    # Section B
    {
        "section": "Section B: Improvement Planning",
        "q": "Q6. After identifying a weakness, how often do you create a specific plan to improve it?",
        "opts": [
            ("Always — I write a plan with clear steps and a timeline", 0),
            ("Usually — I make a plan most of the time", 1),
            ("Sometimes — only when I feel the weakness is serious enough", 2),
            ("Rarely — I tell myself I will improve but rarely plan how", 3),
            ("Never — I do not usually make any plan", 4)
        ]
    },
    {
        "q": "Q7. How specific and detailed are the improvement plans you make?",
        "opts": [
            ("Very specific — I include exact steps, resources, and deadlines", 0),
            ("Fairly specific — I know what I will do but not always when", 1),
            ("Vague — I have a general idea but it is not written down properly", 2),
            ("Very vague — I just tell myself to try harder", 3),
            ("I do not make improvement plans", 4)
        ]
    },
    {
        "q": "Q8. How often do you actually follow through on the improvement plans you make?",
        "opts": [
            ("Almost always — I stick to my plans consistently", 0),
            ("Usually — I follow through more often than not", 1),
            ("About half the time — I start but do not always finish", 2),
            ("Rarely — I make plans but usually do not follow them", 3),
            ("Never — making plans and following them is a real struggle for me", 4)
        ]
    },
    {
        "q": "Q9. Do you set deadlines for yourself when working on a targeted improvement plan?",
        "opts": [
            ("Yes — I always set clear deadlines and track them", 0),
            ("Usually — I set rough deadlines most of the time", 1),
            ("Sometimes — only for the most important goals", 2),
            ("Rarely — I think about deadlines but do not commit to them", 3),
            ("No — I do not set deadlines for personal improvement goals", 4)
        ]
    },
    {
        "q": "Q10. How often do you look back at a previous improvement plan to check whether it worked?",
        "opts": [
            ("Always — reviewing past plans is a regular habit", 0),
            ("Usually — I go back and review most of the time", 1),
            ("Sometimes — only when something reminds me to", 2),
            ("Rarely — I move on to the next thing without reviewing", 3),
            ("Never — I do not look back at plans once I have moved on", 4)
        ]
    },
    # Section C
    {
        "section": "Section C: Self-Monitoring and Progress Awareness",
        "q": "Q11. How well can you judge whether your academic performance has improved over the past month?",
        "opts": [
            ("Very well — I track my progress and can see it clearly", 0),
            ("Fairly well — I have a good general sense of improvement", 1),
            ("Somewhat — I notice big changes but miss smaller ones", 2),
            ("Not well — it is difficult to tell if I am improving", 3),
            ("Not at all — I have no real sense of whether I am getting better", 4)
        ]
    },
    {
        "q": "Q12. When you receive feedback from a teacher, how often do you use it to update your understanding of your own skills?",
        "opts": [
            ("Always — I study all feedback carefully and adjust accordingly", 0),
            ("Usually — I use feedback most of the time", 1),
            ("Sometimes — only when the feedback surprises me", 2),
            ("Rarely — I read it but do not usually act on it", 3),
            ("Never — I do not really pay attention to feedback after receiving it", 4)
        ]
    },
    {
        "q": "Q13. How often do you compare your current academic skills to where you were at the start of the semester?",
        "opts": [
            ("Regularly — I make this comparison at least once a month", 0),
            ("Occasionally — a few times per semester", 1),
            ("Rarely — only if something specific prompts me to", 2),
            ("Almost never — I do not think about progress over time", 3),
            ("Never — I focus only on what is in front of me right now", 4)
        ]
    },
    {
        "q": "Q14. How confident are you that your self-assessment of your skills is accurate?",
        "opts": [
            ("Very confident — I have a realistic and honest view of myself", 0),
            ("Fairly confident — I think I am mostly accurate", 1),
            ("Unsure — I am not really sure how accurate my self-view is", 2),
            ("Not very confident — I think I often misjudge myself", 3),
            ("Not confident at all — I find it hard to assess my own abilities", 4)
        ]
    },
    {
        "q": "Q15. Overall, how much has regular skill auditing and improvement planning helped your academic results?",
        "opts": [
            ("A great deal — it has made a clear difference to my performance", 0),
            ("Somewhat — I think it has helped, though it is hard to measure", 1),
            ("A little — maybe slightly, but nothing dramatic", 2),
            ("Not much — I do not think it has made much difference", 3),
            ("Not at all — or I have never tried it so I cannot say", 4)
        ]
    }
]

psych_states = [
    (10,  "Highly Self-Directed Learner",
          "You consistently audit your skills and follow through with targeted plans. "
          "This is one of the strongest habits a student can build. "
          "Tip: Try mentoring a classmate — teaching others deepens your own self-awareness.",
          "#1a7a4a"),
    (20,  "Active Improver",
          "You engage with self-assessment regularly and usually act on it. "
          "Try making your plans more structured — add deadlines and review whether each plan worked before moving on.",
          "#2e7d32"),
    (30,  "Occasional Assessor",
          "You assess your skills sometimes, but the habit is not consistent yet. "
          "Try scheduling a short monthly review — even 20 minutes can make a real difference across a semester.",
          "#f57f17"),
    (40,  "Passive Learner",
          "You tend to react to academic problems rather than plan ahead. "
          "Start small: after your next assignment, spend 10 minutes writing one skill to improve and one step to take.",
          "#e65100"),
    (50,  "Academically Disengaged",
          "Very little self-assessment is happening right now. "
          "This is likely affecting your academic performance. Consider talking to a tutor or academic advisor this week.",
          "#b71c1c"),
    (60,  "At Risk — Support Needed",
          "No meaningful skill monitoring or improvement planning is taking place. "
          "Please reach out to your university's academic support services. Small changes can make a big difference.",
          "#880e4f"),
]

def get_result(score):
    for threshold, state, recommendation, color in psych_states:
        if score <= threshold:
            return state, recommendation, color
    return psych_states[-1][1], psych_states[-1][2], psych_states[-1][3]

def validate_name(name):
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

# ---------------- UI ----------------
st.title("📊 Monthly Academic Skill Audit")
st.subheader("Targeted Improvement Plan Questionnaire")
st.markdown("**Topic #180 | WIUT | Fundamentals of Programming**")
st.markdown("---")
st.info("Answer each question honestly. There are no right or wrong answers. Your score will tell you which academic state you are in and what you can do about it.")

# --- User Info ---
st.markdown("### Your Details")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name")
    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
with col2:
    surname = st.text_input("Surname")
    sid = st.text_input("Student ID")

st.markdown("---")

# --- Questions ---
st.markdown("### Survey Questions")
st.caption("Select one answer per question (0 = best habit, 4 = worst habit)")

answers = []
current_section = ""
all_answered = True

for idx, q in enumerate(questions):
    if "section" in q and q["section"] != current_section:
        current_section = q["section"]
        st.markdown(f"#### {current_section}")

    labels = [opt[0] for opt in q["opts"]]
    choice = st.radio(q["q"], labels, key=f"q{idx}", index=None)

    if choice is None:
        all_answered = False
    else:
        score = next(s for label, s in q["opts"] if label == choice)
        answers.append({"question": q["q"], "answer": choice, "score": score})

st.markdown("---")

# --- Submit ---
if st.button("Submit Survey", type="primary"):
    errors = []
    if not validate_name(name):
        errors.append("Please enter a valid given name (no numbers).")
    if not validate_name(surname):
        errors.append("Please enter a valid surname (no numbers).")
    if not validate_dob(dob):
        errors.append("Date of birth must be in YYYY-MM-DD format.")
    if not sid.strip():
        errors.append("Please enter your student ID.")
    if not all_answered:
        errors.append("Please answer all 15 questions before submitting.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        total_score = sum(a["score"] for a in answers)
        state, recommendation, color = get_result(total_score)

        st.markdown("---")
        st.markdown("## ✅ Your Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Score", f"{total_score} / 60")
        with col2:
            st.metric("Questions Answered", f"{len(answers)} / 15")

        st.markdown(
            f"<div style='background-color:{color};padding:20px;border-radius:10px;color:white;'>"
            f"<h3 style='color:white;margin:0'>🎯 {state}</h3>"
            f"<p style='margin-top:10px;color:white;'>{recommendation}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": state,
            "recommendation": recommendation,
            "answers": answers,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.download_button(
            label="⬇️ Download My Results (JSON)",
            data=json.dumps(record, indent=2),
            file_name=f"{sid}_skill_audit_result.json",
            mime="application/json"
        )

        st.success("Survey completed successfully. You can download your results above.")
