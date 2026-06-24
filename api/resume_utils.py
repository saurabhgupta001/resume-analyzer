import pdfplumber
import docx
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skill_data import SKILLS


# =========================================
# Extract Text from PDF
# =========================================

def extract_pdf_text(file_path):

    text = ''

    try:

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + ' '

    except Exception as e:

        print("PDF Extraction Error:", str(e))

    return text


# =========================================
# Extract Text from DOCX
# =========================================

def extract_docx_text(file_path):

    text = ''

    try:

        doc = docx.Document(file_path)

        for para in doc.paragraphs:

            text += para.text + ' '

    except Exception as e:

        print("DOCX Extraction Error:", str(e))

    return text


# =========================================
# Clean Text
# =========================================

def clean_text(text):

    if not text:
        return ''

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9@+#.\-\s]',
        ' ',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


# =========================================
# Extract Skills
# =========================================

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        skill_lower = skill.lower()

        if skill_lower in text:

            found_skills.append(skill_lower)

    return list(set(found_skills))


# =========================================
# Calculate Resume Match Score
# =========================================

def calculate_similarity(
    resume_text,
    jd_text,
    resume_skills=None,
    jd_skills=None
):

    try:

        if not resume_text or not jd_text:
            return 0

        matched_skills = len(
            set(resume_skills).intersection(
                set(jd_skills)
            )
        )

        if len(jd_skills) > 0:

            skill_score = (
                matched_skills / len(jd_skills)
            ) * 100

        else:

            skill_score = 0

        documents = [
            resume_text,
            jd_text
        ]

        tfidf = TfidfVectorizer()

        matrix = tfidf.fit_transform(
            documents
        )

        text_similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0] * 100

        final_score = (
            (skill_score * 0.85)
            +
            (text_similarity * 0.15)
        )

        # Smart Boost

        if matched_skills >= 1 and final_score < 60:

            final_score = 60 + (
                matched_skills * 8
            )

        if matched_skills >= 3 and final_score < 75:

            final_score = 75 + (
                matched_skills * 3
            )

        if final_score > 100:
            final_score = 100

        return round(final_score, 2)

    except Exception as e:

        print(
            "Similarity Error:",
            str(e)
        )

        return 0
# =========================================
# Missing Skills
# =========================================

def missing_skills(
    resume_skills,
    jd_skills
):

    missing = list(
        set(jd_skills) - set(resume_skills)
    )

    if not missing:

        return ["No missing skills"]

    return missing


# =========================================
# Advanced ATS Score
# =========================================

def calculate_ats_score(
    resume_text,
    resume_skills,
    jd_skills
):

    total_score = 0

    # =====================================
    # 1. Skill Matching -> 40 Marks
    # =====================================

    skill_score = 0

    if jd_skills:

        matched_skills = len(
            set(resume_skills).intersection(
                set(jd_skills)
            )
        )

        skill_score = (
            matched_skills / len(jd_skills)
        ) * 40
    
    total_score += skill_score

    # =====================================
    # 2. Experience -> 10 Marks
    # =====================================

    experience_keywords = [
        'experience',
        'internship',
        'worked',
        'employment',
        'company'
    ]

    found_exp = 0

    for word in experience_keywords:

        if word in resume_text:
            found_exp += 1

    experience_score = min(
        found_exp * 5,
        10
    )
    total_score += experience_score

    # =====================================
    # 3. Projects -> 20 Marks
    # =====================================

    project_keywords = [
        'project',
        'projects',
        'developed',
        'built',
        'portfolio'
    ]

    found_projects = 0

    for word in project_keywords:

        if word in resume_text:
            found_projects += 1

    project_score = min(
        found_projects * 7,
        20
    )
    total_score += project_score

    # =====================================
    # 4. Certifications -> 10 Marks
    # =====================================

    certification_keywords = [
        'certification',
        'certificate',
        'certified',
        'course'
    ]

    found_certifications = 0

    for word in certification_keywords:

        if word in resume_text:
            found_certifications += 1

    certification_score = min(
        found_certifications * 2.5,
        10
    )
    total_score += certification_score

    # =====================================
    # 5. Resume Formatting -> 10 Marks
    # =====================================

    sections = [
        'education',
        'skills',
        'experience',
        'projects',
        'certification'
    ]

    found_sections = 0

    for section in sections:

        if section in resume_text:
            found_sections += 1

    formatting_score = (
        found_sections / len(sections)
    ) * 10
    total_score += formatting_score

    # =====================================
    # 6. Grammar / Resume Length -> 10 Marks
    # =====================================

    word_count = len(
        resume_text.split()
    )

    if word_count >= 300:

        grammar_score = 10

    elif word_count >= 200:

        grammar_score = 8

    elif word_count >= 100:

        grammar_score = 6

    elif word_count >= 50:

        grammar_score = 2

    else:

        grammar_score = 1
    total_score += grammar_score

    # =====================================
    # Final Score
    # =====================================

    if total_score > 100:
        total_score = 100

    return round(total_score, 2)


# =========================================
# AI ATS Feedback Generator
# =========================================

def generate_ai_feedback(
    ats_score,
    missing_skills,
    errors,
    raw_resume_text
):

    feedback = []

    resume_text = raw_resume_text.lower()

    # =====================================
    # ATS SCORE FEEDBACK
    # =====================================

    if ats_score >= 85:

        feedback.append(
            "Excellent ATS score. Your resume is well optimized."
        )

    elif ats_score >= 70:

        feedback.append(
            "Good ATS score but some sections can still be improved."
        )

    elif ats_score >= 50:

        feedback.append(
            "Average ATS score. Resume needs better optimization."
        )

    else:

        feedback.append(
            "Low ATS score. Major improvements are required."
        )

    # =====================================
    # MISSING SKILLS FEEDBACK
    # =====================================

    if (
        missing_skills and
        len(missing_skills) > 0 and
        missing_skills[0] != "No missing skills"
    ):

        feedback.append(
            "Add more relevant technical skills from the job description."
        )

    # =====================================
    # PROJECTS ANALYSIS
    # =====================================

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "portfolio"
    ]

    has_projects = False

    for word in project_keywords:

        if word in resume_text:

            has_projects = True
            break

    if not has_projects:

        feedback.append(
            "Add strong projects section with real-world projects."
        )

    # =====================================
    # EXPERIENCE ANALYSIS
    # =====================================

    experience_keywords = [
        "internship",
        "employment"
    ]

    has_experience = False

    for word in experience_keywords:

        if word in resume_text:

            has_experience = True
            break

    if not has_experience:

        feedback.append(
            "Add internship, freelance work, or practical experience."
        )

    # =====================================
    # CERTIFICATION ANALYSIS
    # =====================================

    certification_keywords = [
        "certification",
        "certificate",
        "certified",
        "course"
    ]

    has_certification = False

    for word in certification_keywords:

        if word in resume_text:

            has_certification = True
            break

    if not has_certification:

        feedback.append(
            "Add certifications or online courses to improve credibility."
        )

    # =====================================
    # STRUCTURE ANALYSIS
    # =====================================

    required_sections = [
        "education",
        "skills",
        "projects"
    ]

    missing_sections = []

    for section in required_sections:

        if section not in resume_text:

            missing_sections.append(section)

    if len(missing_sections) > 0:

        feedback.append(
            "Improve resume structure by adding sections like: "
            + ", ".join(missing_sections)
        )

    # =====================================
    # RESUME LENGTH ANALYSIS
    # =====================================

    word_count = len(
        resume_text.split()
    )

    if word_count < 80:

        feedback.append(
            "Resume content is too short. Add more achievements and technical details."
        )

    elif word_count > 800:

        feedback.append(
            "Resume is too lengthy. Keep it concise and relevant."
        )

    # =====================================
    # LINKEDIN ANALYSIS
    # =====================================

    if "linkedin" not in resume_text:

        feedback.append(
            "Add LinkedIn profile for better professional visibility."
        )

    # =====================================
    # EMAIL ANALYSIS
    # =====================================

    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

    emails = re.findall(
        email_pattern,
        raw_resume_text,
        re.IGNORECASE
    )

    valid_email_found = False

    for email in emails:

        email = email.strip().lower()

        fake_words = [
            "example",
            "yourname",
            "sample",
            "test",
            "demo"
        ]

        is_fake = any(
            word in email
            for word in fake_words
        )

        if (
            not is_fake
            and "@" in email
            and "." in email.split("@")[-1]
        ):

            valid_email_found = True
            break

    if not valid_email_found:

        feedback.append(
            "Add a professional email address."
        )

    # =====================================
    # PHONE ANALYSIS
    # =====================================

    phone_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'

    if not re.findall(phone_pattern, raw_resume_text):

        feedback.append(
            "Add phone number for recruiter communication."
        )

    # =====================================
    # FINAL DEFAULT FEEDBACK
    # =====================================

    if len(feedback) == 0:

        feedback.append(
            "Your resume looks strong and ATS friendly."
        )

    return feedback


# =========================================
# Find Resume Errors
# =========================================

def find_resume_errors(text):

    errors = []

    if not text:

        return [
            "Resume text not extracted properly"
        ]

    text_lower = text.lower()

    # =====================================
    # Email Check
    # =====================================

    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

    emails = re.findall(
        email_pattern,
        text,
        re.IGNORECASE
    )

    valid_email_found = False

    for email in emails:

        invalid_words = [
            "example",
            "sample",
            "test",
            "yourname"
        ]

        if not any(word in email.lower() for word in invalid_words):

            valid_email_found = True
            break

    if not valid_email_found:

        errors.append(
            "Professional email address not found"
        )

    # =====================================
    # Phone Check
    # =====================================

    phone_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'

    if not re.findall(phone_pattern, text):

        errors.append(
            "Phone number not found"
        )

    # =====================================
    # LinkedIn Check
    # =====================================

    if 'linkedin' not in text_lower:

        errors.append(
            "LinkedIn profile missing"
        )

    # =====================================
    # Projects Check
    # =====================================

    if 'project' not in text_lower:

        errors.append(
            "Projects section missing"
        )

    # =====================================
    # Experience Check
    # =====================================

    if 'experience' not in text_lower:

        errors.append(
            "Experience section missing"
        )

    # =====================================
    # Resume Length Check
    # =====================================

    if len(text.split()) < 80:

        errors.append(
            "Resume content is too short"
        )

    # =====================================
    # Final Default
    # =====================================

    if len(errors) == 0:

        errors.append(
            "No major errors found"
        )

    return errors


# =========================================
# Job Recommendations
# =========================================

def recommend_jobs(skills):

    jobs = []

    skills = [
        skill.lower()
        for skill in skills
    ]

    if (
        'python' in skills and
        'django' in skills
    ):

        jobs.append(
            'Backend Django Developer'
        )

    if (
        'javascript' in skills and
        'react' in skills
    ):

        jobs.append(
            'Frontend React Developer'
        )

    if 'machine learning' in skills:

        jobs.append(
            'Machine Learning Engineer'
        )

    if 'mongodb' in skills:

        jobs.append(
            'MongoDB Database Developer'
        )

    if (
        'html' in skills and
        'css' in skills
    ):

        jobs.append(
            'Web Designer'
        )

    if 'rest api' in skills:

        jobs.append(
            'API Developer'
        )

    if 'sql' in skills:

        jobs.append(
            'SQL Developer'
        )

    if 'communication' in skills:

        jobs.append(
            'Communication Specialist'
        )

    if 'sales' in skills:

        jobs.append(
            'Sales Executive'
        )
    if 'python' in skills:

        jobs.append(
            'Python Developer'
        )
    if 'Java' in skills:

        jobs.append(
            'Java developer'
        )
    if 'HTML' in skills and 'CSS' in skills and 'Javascript' in skills:

        jobs.append(
            'Frontend Developer'
        )
    if 'python' in skills and 'numpy' in skills and 'pandas' in skills and 'matplot' in skills and 'ML' in skills:

        jobs.append(
            'Data Analyst'
        )

    if 'C++' in skills:

        jobs.append(
            'C++ developer'
        )
    if 'AI' in skills:

        jobs.append(
            'AI Engineer'
        )
    
    if (
        'financial analysis' in skills or
        'accounting' in skills
    ):

        jobs.append(
            'Financial Analyst'
        )

    if not jobs:

        jobs.append(
            'Software Developer'
        )

    return jobs