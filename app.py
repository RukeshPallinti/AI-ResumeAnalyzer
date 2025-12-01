import streamlit as st
import pdfplumber
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "nlp"))
from nlp.extractor import analyze_resume
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🤖 AI Resume Skill Extractor & Analyzer")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF or TXT)", type=["pdf", "txt"])
skills_list = [line.strip() for line in open("data/skills.txt").readlines()]
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = " "
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    if text:
        st.success("✅ Resume uploaded successfully!")
        results = analyze_resume(text, skills_list)

        st.subheader("📋 Extracted Resume Details")
        st.json(results)

        if results["Skills"]:
            st.bar_chart({"Skills": [len(results["Skills"])]})

        st.download_button(
            label="⬇️ Download JSON Result",
            data=str(results),
            file_name="resume_analysis.json",
            mime="application/json"
        )
    else:
        st.error("Could not extract text from the resume.")
