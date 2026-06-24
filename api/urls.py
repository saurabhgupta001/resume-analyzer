from django.urls import path
from .views import (
    home,
    ResumeAnalyzerView,
    result_page,
    analytics_dashboard
)
from . import views

urlpatterns = [

    # ==============================
    # Home Page
    # ==============================
    path(
        '',
        home,
        name='home'
    ),

    # ==============================
    # Resume Analyzer API
    # ==============================
    path(
        'analyze/',
        ResumeAnalyzerView.as_view(),
        name='analyze'
    ),

    # ==============================
    # Result Dashboard
    # ==============================
    path(
        'result/',
        result_page,
        name='result_page'
    ),

    # ==============================
    # Recommended Jobs
    # ==============================
    path(
        'recommended-jobs/',
        views.recommended_jobs,
        name='recommended_jobs'
    ),

    # ==============================
    # About Page
    # ==============================
    path(
        'about/',
        views.about,
        name='about'
    ),

    # ==============================
    # Contact Page
    # ==============================
    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    # ==============================
    # Resume Templates
    # ==============================
    path(
        'templates/',
        views.templates,
        name='templates'
    ),

    # ==============================
    # Admin Analytics Dashboard
    # ==============================
    path(
        'analytics/',
        analytics_dashboard,
        name='analytics_dashboard'
    ),

]