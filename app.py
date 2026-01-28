import streamlit as st
import pdfplumber
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "nlp"))
from nlp.extractor import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🤖 AI Resume Skill Extractor & Analyzer")

uploaded_file = st.file_uploader(
    "📤 Upload your resume (PDF or TXT)",
    type=["pdf", "txt"]
)

st.subheader("📝 Job Description")
jd_text = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder="Paste the job description here..."
)

# Analyze button
analyze_clicked = st.button("🔍 Analyze Resume")

skills_list = [line.strip() for line in open("data/skills.txt").readlines()]

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ================= ANALYSIS =================
if analyze_clicked:

    if not uploaded_file:
        st.warning("⚠️ Please upload a resume file.")
        st.stop()

    # Read resume text
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    if not resume_text.strip():
        st.error("❌ Could not extract text from the resume.")
        st.stop()

    st.success("✅ Resume uploaded successfully!")

    results = analyze_resume(resume_text, skills_list, jd_text)

    # ================= Scores =================
    st.subheader("📊 Resume Scores")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Quality Score", f"{results['Resume_Score']} / 100")
        st.progress(results["Resume_Score"] / 100)

    with col2:
        st.metric("JD Match Score", f"{results['Job_Match_Score']} %")
        st.progress(results["Job_Match_Score"] / 100)

    # ================= Skill Breakdown =================
    st.subheader("🧠 Skill Match Breakdown")

    st.write("✅ Matched Skills")
    st.success(", ".join(results["Matched_Skills"]) or "None")

    st.write("❌ Missing Skills")
    st.error(", ".join(results["Missing_Skills"]) or "None")

    st.write("➕ Extra Skills")
    st.info(", ".join(results["Extra_Skills"]) or "None")

    # ================= JSON Output =================
    st.subheader("📋 Extracted Resume Details (JSON)")
    st.json(results)

    st.download_button(
        label="⬇️ Download JSON Result",
        data=str(results),
        file_name="resume_analysis.json",
        mime="application/json"
    )
