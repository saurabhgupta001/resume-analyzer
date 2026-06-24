from django.db import models


class Resume(models.Model):

    # =====================================
    # Resume Information
    # =====================================

    resume_file = models.FileField(
        upload_to='resumes/'
    )

    job_description = models.TextField()

    # =====================================
    # Scores
    # =====================================

    ats_score = models.FloatField(
        default=0
    )

    resume_match_score = models.FloatField(
        default=0
    )

    # =====================================
    # Analytics Data
    # =====================================

    resume_skills = models.TextField(
        blank=True
    )

    missing_skills = models.TextField(
        blank=True
    )

    recommended_jobs = models.TextField(
        blank=True
    )

    ai_feedback = models.TextField(
        blank=True
    )

    errors = models.TextField(
        blank=True
    )

    # =====================================
    # Upload Date
    # =====================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.resume_file.name