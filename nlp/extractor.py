import re

def analyze_resume(text, skills_list):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # ------------------------ NAME ------------------------
    name = lines[0] if lines else " "

    # ------------------------ EMAIL ------------------------
    email = None
    email_matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}", text)
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
    for line in lines:
        if "education" in line.lower():
            collect_edu = True
            continue
        if collect_edu:
            if any(w in line.lower() for w in ["skills", "projects", "soft"]):
                break
            if any(w in line.lower() for w in ["b.tech", "intermediate", "secondary", "degree"]):
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
                # Only take first title lines
                if not line.lower().startswith(("developed", "built", "created", "designed", "analyzed")):
                    projects.append(line)

    projects = list(dict.fromkeys(projects))  # Remove duplicates

    # ------------------------ SKILLS ------------------------
    extracted_skills = []
    text_lower = text.lower()

    for skill in skills_list:
        if skill.lower() in text_lower:
            extracted_skills.append(skill)

    extracted_skills = list(dict.fromkeys(extracted_skills))  # Remove duplicates

    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Education": education,
        "Skills": extracted_skills,
        "Projects": projects
    }
