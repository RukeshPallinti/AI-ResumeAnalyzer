# 🤖 AI Resume Analyzer (spaCy + Streamlit)

This is a beginner-friendly project that extracts important details from a resume such as:

- Name  
- Email  
- Phone number  
- Skills  
- Education  
- Projects  

The project uses:
- **spaCy** for basic NLP  
- **Streamlit** for the UI  
- **pdfplumber** to read PDF files  
- Simple custom Python functions  

The entire code is kept easy to understand so beginners can learn step-by-step.

## 📂 Project Structure

resume-analyzer/
│
├── app.py # Streamlit app (frontend)
├── nlp/
│ └── extractor.py # spaCy-based resume extractor
└── data/
└── skills.txt # Skill keywords for matching
---

## ✨ Features

✔ Upload a **PDF** or **TXT** resume  
✔ Uses **spaCy NER** to detect names  
✔ Extracts email & phone numbers using regex  
✔ Matches skills using **spaCy PhraseMatcher**  
✔ Extracts Education and Projects using simple rules  
✔ Shows extracted details in JSON format  
✔ Easy and beginner-friendly code  

 🚀 Installation

1️⃣ Install required libraries
pip install streamlit pdfplumber spacy

2️⃣Download the spaCy model
streamlit run app.py

3️⃣ Run the Streamlit app
streamlit run app.py
  
🧠 How It Works (Simple Explanation)
✔ spaCy NER
Used to find names in the resume.

✔ spaCy PhraseMatcher
Used to match skills (loaded from skills.txt).

✔ Regex
Used for:
finding email
finding phone numbers

✔ Rule-Based Section Detection
Used for:
Education
Projects
Everything is intentionally simple so beginners can understand the logic.
