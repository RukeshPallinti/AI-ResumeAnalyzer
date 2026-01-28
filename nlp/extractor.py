import re

def analyze_resume(text, skills_list, jd_text=None):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # ------------------------ NAME ------------------------
    name = lines[0] if lines else ""

    # ------------------------ EMAIL ------------------------
    email = None
    email_matches = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}", text
    )
    if email_matches:
        email = email_matches[0]

    # ------------------------ PHONE ------------------------
    phone = None
    phone_matches = re.findall(r"\b[6-9]\d{9}\b", text)
    if phone_matches:
        phone = phone_matches[0]

    # ------------------------ EDUCATION ------------------------
    education = []
    collect_edu = False

    EDU_KEYWORDS = [
        "b.tech", "btech", "b.e", "be", "bachelor",
        "b.sc", "bsc", "bca", "b.com", "bcom",
        "undergraduate", "ug", "degree",
        "engineering", "technology",
        "intermediate", "secondary"
    ]

    for line in lines:
        line_lower = line.lower()

        if "education" in line_lower:
            collect_edu = True
            continue

        if collect_edu:
            if any(w in line_lower for w in ["skills", "projects", "experience", "certification"]):
                break

            if any(k in line_lower for k in EDU_KEYWORDS):
                education.append(line)

    # ------------------------ PROJECTS ------------------------
    projects = []
    collect_proj = False
    for line in lines:
        if "projects" in line.lower():
            collect_proj = True
            continue
        if collect_proj:
            if "education" in line.lower():
                break
            if len(line) > 3 and not line.startswith(("•", "-", "*")):
                if not line.lower().startswith(
                    ("developed", "built", "created", "designed", "analyzed")
                ):
                    projects.append(line)

    projects = list(dict.fromkeys(projects))  # remove duplicates

    # ------------------------ SKILLS (Resume) ------------------------
    extracted_skills = []
    text_lower = text.lower()

    for skill in skills_list:
        if skill.lower() in text_lower:
            extracted_skills.append(skill)

    extracted_skills = list(dict.fromkeys(extracted_skills))

    # ------------------------ JD ANALYSIS ------------------------
    jd_skills = []
    if jd_text:
        jd_text_lower = jd_text.lower()
        for skill in skills_list:
            if skill.lower() in jd_text_lower:
                jd_skills.append(skill)

    jd_skills = list(dict.fromkeys(jd_skills))

    # ------------------------ SKILL MATCHING ------------------------
    resume_skills_set = set(extracted_skills)
    jd_skills_set = set(jd_skills)

    matched_skills = list(resume_skills_set & jd_skills_set)
    missing_skills = list(jd_skills_set - resume_skills_set)
    extra_skills = list(resume_skills_set - jd_skills_set)

    # ------------------------ JD MATCH SCORE ------------------------
    if len(jd_skills_set) > 0:
        job_match_score = round((len(matched_skills) / len(jd_skills_set)) * 100, 2)
    else:
        job_match_score = 0

    # ------------------------ RESUME QUALITY SCORE ------------------------
    resume_score = 0

    if extracted_skills:
        resume_score += 30

    if education:
        resume_score += 15

    if projects:
        resume_score += 25

    if len(extracted_skills) >= 8:
        resume_score += 15

    resume_score = min(resume_score, 100)

    # ------------------------ FINAL OUTPUT ------------------------
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Education": education,
        "Skills": extracted_skills,
        "Projects": projects,

        # New fields
        "Resume_Score": resume_score,
        "Job_Match_Score": job_match_score,
        "Matched_Skills": matched_skills,
        "Missing_Skills": missing_skills,
        "Extra_Skills": extra_skills
    }
