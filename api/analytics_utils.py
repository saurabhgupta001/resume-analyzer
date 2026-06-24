import matplotlib
# Use a non-GUI backend
matplotlib.use("Agg")
import base64
from io import BytesIO
from collections import Counter

import pandas as pd

import matplotlib.pyplot as plt


# ==========================================
# Convert Matplotlib Figure to Base64
# ==========================================

def get_graph():

    buffer = BytesIO()

    plt.tight_layout()

    plt.savefig(buffer, format="png")

    buffer.seek(0)

    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png).decode("utf-8")

    buffer.close()

    plt.close()

    return graph


# ==========================================
# ATS Score Distribution
# ==========================================

def ats_distribution_chart(df):

    if df.empty:
        return None

    plt.figure(figsize=(7, 4))

    plt.hist(
        df["ats_score"],
        bins=10
    )

    plt.title("ATS Score Distribution")

    plt.xlabel("ATS Score")

    plt.ylabel("Number of Resumes")

    return get_graph()


# ==========================================
# Resume Upload Trend
# ==========================================

def upload_trend_chart(df):

    if df.empty:
        return None

    # Convert to datetime
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Remove timezone if present
    if df["created_at"].dt.tz is not None:
        df["created_at"] = df["created_at"].dt.tz_localize(None)

    uploads = df.groupby(
        df["created_at"].dt.date
    ).size()

    plt.figure(figsize=(8, 4))

    plt.plot(
        uploads.index,
        uploads.values,
        marker="o"
    )

    plt.title("Resume Upload Trend")

    plt.xlabel("Date")

    plt.ylabel("Uploads")

    plt.xticks(rotation=30)

    return get_graph()


# ==========================================
# Top Resume Skills
# ==========================================

def top_skills_chart(df):

    if df.empty:
        return None

    skills = []

    for row in df["resume_skills"]:

        if row:

            skills.extend(
                [skill.strip() for skill in row.split(",")]
            )

    counter = Counter(skills)

    top = counter.most_common(10)

    labels = [item[0] for item in top]

    values = [item[1] for item in top]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("Top Resume Skills")

    plt.xticks(rotation=30)

    return get_graph()


# ==========================================
# Missing Skills
# ==========================================

def missing_skills_chart(df):

    if df.empty:
        return None

    skills = []

    for row in df["missing_skills"]:

        if row:

            skills.extend(
                [skill.strip() for skill in row.split(",")]
            )

    counter = Counter(skills)

    top = counter.most_common(10)

    labels = [item[0] for item in top]

    values = [item[1] for item in top]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("Most Missing Skills")

    plt.xticks(rotation=30)

    return get_graph()


# ==========================================
# Recommended Jobs
# ==========================================

def recommended_jobs_chart(df):

    if df.empty:
        return None

    jobs = []

    for row in df["recommended_jobs"]:

        if row:

            jobs.extend(
                [job.strip() for job in row.split(",")]
            )

    counter = Counter(jobs)

    top = counter.most_common(6)

    labels = [item[0] for item in top]

    values = [item[1] for item in top]

    plt.figure(figsize=(6, 6))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    plt.title("Recommended Jobs")

    return get_graph()