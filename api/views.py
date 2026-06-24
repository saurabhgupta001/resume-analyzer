from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Resume

# =========================
# NLP + ML IMPORTS (NEW)
# =========================
from .nlp_utils import preprocess_text, extract_entities
from .ml_utils import match_score

# =========================
# YOUR EXISTING IMPORTS
# =========================
from .resume_utils import (
    extract_pdf_text,
    extract_docx_text,
    clean_text,
    extract_skills,
    calculate_similarity,
    missing_skills,
    calculate_ats_score,
    generate_ai_feedback,
    find_resume_errors,
    recommend_jobs
)

from .analytics import (
    get_resume_dataframe,
    overall_statistics,
    upload_statistics,
    ats_categories
)

from .analytics_utils import (
    ats_distribution_chart,
    upload_trend_chart,
    top_skills_chart,
    missing_skills_chart,
    recommended_jobs_chart,
)

# =========================================================
# FRONTEND PAGES
# =========================================================

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def templates(request):
    return render(request, "resume_temp.html")


def result_page(request):
    return render(request, 'result.html')


def recommended_jobs(request):
    job = request.GET.get('job', '')
    return render(request, "recommended_jobs.html", {"job": job})


# =========================================================
# ANALYTICS DASHBOARD
# =========================================================

def analytics_dashboard(request):

    df = get_resume_dataframe()

    context = {
        "stats": overall_statistics(df),
        "uploads": upload_statistics(df),
        "categories": ats_categories(df),

        "ats_chart": ats_distribution_chart(df),
        "upload_chart": upload_trend_chart(df),
        "skills_chart": top_skills_chart(df),
        "missing_chart": missing_skills_chart(df),
        "jobs_chart": recommended_jobs_chart(df),
    }

    return render(request, "analytics.html", context)


# =========================================================
# MAIN AI RESUME ANALYZER API
# =========================================================

class ResumeAnalyzerView(APIView):

    def post(self, request):

        try:

            # =========================
            # INPUT DATA
            # =========================

            resume_file = request.FILES.get('resume_file')
            job_description = request.data.get('job_description', '')

            if not resume_file:
                return Response(
                    {'success': False, 'error': 'Resume file is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # =========================
            # SAVE FILE
            # =========================

            resume = Resume.objects.create(
                resume_file=resume_file,
                job_description=job_description
            )

            file_path = resume.resume_file.path

            # =========================
            # TEXT EXTRACTION
            # =========================

            if file_path.endswith('.pdf'):
                resume_text = extract_pdf_text(file_path)

            elif file_path.endswith('.docx'):
                resume_text = extract_docx_text(file_path)

            else:
                return Response(
                    {'success': False, 'error': 'Only PDF and DOCX supported'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not resume_text:
                return Response(
                    {'success': False, 'error': 'Unable to extract resume text'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            raw_resume_text = resume_text

            # =========================
            # CLEANING
            # =========================

            cleaned_resume_text = clean_text(resume_text)
            cleaned_job_description = clean_text(job_description)

            # =========================
            # 🧠 NLP (spaCy)
            # =========================

            nlp_resume = preprocess_text(cleaned_resume_text)
            nlp_jd = preprocess_text(cleaned_job_description)

            entities = extract_entities(cleaned_resume_text)

            # =========================
            # SKILL EXTRACTION
            # =========================

            resume_skills = extract_skills(cleaned_resume_text)
            jd_skills = extract_skills(cleaned_job_description)

            # =========================
            # 🤖 ML (scikit-learn)
            # =========================

            ml_score = match_score(
                cleaned_resume_text,
                cleaned_job_description
            )

            # =========================
            # RULE-BASED SCORE
            # =========================

            rule_score = calculate_similarity(
                cleaned_resume_text,
                cleaned_job_description,
                resume_skills,
                jd_skills
            )

            # fallback
            if rule_score == 0:
                matched_skills = len(
                    set(resume_skills).intersection(set(jd_skills))
                )

                if len(jd_skills) > 0:
                    rule_score = (matched_skills / len(jd_skills)) * 100

            # =========================
            # FINAL HYBRID SCORE
            # =========================

            final_score = (0.6 * rule_score) + (0.4 * ml_score)

            # =========================
            # ATS SCORE
            # =========================

            ats_score = calculate_ats_score(
                cleaned_resume_text,
                resume_skills,
                jd_skills
            )

            # =========================
            # ANALYSIS
            # =========================

            missing = missing_skills(resume_skills, jd_skills)
            errors = find_resume_errors(raw_resume_text)

            ai_feedback = generate_ai_feedback(
                ats_score,
                missing,
                errors,
                raw_resume_text
            )

            recommended = recommend_jobs(resume_skills)

            # =========================
            # SAVE TO DB
            # =========================

            resume.ats_score = ats_score
            resume.resume_match_score = final_score
            resume.resume_skills = ",".join(resume_skills or [])
            resume.missing_skills = ",".join(missing or [])
            resume.recommended_jobs = ",".join(recommended or [])
            resume.ai_feedback = "\n".join(ai_feedback or [])
            resume.errors = "\n".join(errors or [])

            resume.save()

            # =========================
            # RESPONSE
            # =========================

            return Response({
                "success": True,

                # scores
                "ats_score": round(ats_score, 2),
                "rule_based_score": round(rule_score, 2),
                "ml_score": round(ml_score, 2),
                "final_score": round(final_score, 2),

                # NLP output
                "entities": entities,

                # skills
                "resume_skills": resume_skills,
                "job_skills": jd_skills,
                "missing_skills": missing,

                # feedback
                "errors": errors,
                "ai_feedback": ai_feedback,

                # jobs
                "recommended_jobs": recommended,

                # breakdown
                "ats_breakdown": {
                    "skills": "40%",
                    "experience": "20%",
                    "projects": "15%",
                    "certifications": "10%",
                    "formatting": "10%",
                    "grammar": "5%"
                }
            })

        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )