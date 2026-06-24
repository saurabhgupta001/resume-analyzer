
# ATSPro – AI Resume Analyzer

ATSPro is an AI-powered Resume Analyzer built with Django + Machine Learning (scikit-learn + spaCy) that evaluates resumes against job descriptions and provides an ATS score, skill matching, missing skills, and improvement feedback.

It also provides personalized job role recommendations based on extracted skills, helping users understand their career fit and improve their resumes effectively.

# 🚀 Live Demo

👉 https://atspro-pwzi.onrender.com

# ✨ Features

📊 ATS Score Calculation (0–100)

🧠 AI-based Resume vs Job Description Matching

🔍 Skill Extraction from Resume

❌ Missing Skills Detection

📝 Resume Quality Feedback (AI suggestions)

📄 PDF & DOCX Resume Support

⚡ Fast TF-IDF based similarity scoring

🎯 Job Role Recommendations

📱 Simple and clean UI

# 🛠️ Tech Stack

Django
ML / NLP
scikit-learn (TF-IDF, cosine similarity)
spaCy (NLP processing)
pdfplumber (PDF parsing)
python-docx (DOCX parsing)
regex (text cleaning)
Frontend
HTML
CSS
JavaScript

# 📁 Project Structure

ATSPro/

│

├── core/                # Django project settings

├── api/                 # Main application

│      ├── views.py

│      ├── resume_utils.py # Core AI logic

│      ├── ml_utils.py     # Matching algorithm

│      └── skill_data.py   # Skills database

│

├── templates/

├── static/

├── manage.py

└── requirements.txt


# How It Works
User Upload Resume

        ↓
Extract Text (PDF/DOCX)

        ↓
Clean & Preprocess Text

        ↓
Extract Skills using NLP

        ↓
Compare with Job Description (TF-IDF)

        ↓
Generate:

   ✔ ATS Score

   ✔ Missing Skills

   ✔ AI Feedback

   ✔ Job Recommendations


   # 📊 Scoring System

🔹 Skill Match → 40%

🔹 Experience → 10%

🔹 Projects → 20%

🔹 Certifications → 10%

🔹 Formatting → 10%

🔹 Resume Length → 10%

# ⚠️ Known Issues

Free hosting may cause slow startup (cold start)

Heavy ML libraries may increase memory usage

First request may take slightly longer

💡 Future Improvements

🌟 Upgrade to deep learning-based matching (BERT)

📈 Advanced ATS scoring dashboard

☁️ Cloud storage for resumes

# 👨‍💻 Author

Saurabh Gupta

GitHub: https://github.com/saurabhgupta001

LinkedIn: https://www.linkedin.com/in/saurabh-gupta-42736432a/

