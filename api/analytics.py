import pandas as pd

from .models import Resume


# ==========================================
# Load Resume Data into Pandas DataFrame
# ==========================================

def get_resume_dataframe():

    queryset = Resume.objects.all().values()

    df = pd.DataFrame(queryset)

    return df
# ==========================================
# Overall Dashboard Statistics
# ==========================================

def overall_statistics(df):

    if df.empty:

        return {

            "total_resumes": 0,

            "average_ats": 0,

            "highest_ats": 0,

            "lowest_ats": 0
        }

    return {

        "total_resumes": len(df),

        "average_ats": round(
            df["ats_score"].mean(),
            2
        ),

        "highest_ats": round(
            df["ats_score"].max(),
            2
        ),

        "lowest_ats": round(
            df["ats_score"].min(),
            2
        )

    }
# ==========================================
# Resume Upload Trend
# ==========================================

def upload_statistics(df):

    if df.empty:

        return {}

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    uploads = (

        df.groupby(

            df["created_at"].dt.date

        ).size()

    )

    return uploads.to_dict()

# ==========================================
# ATS Categories
# ==========================================

def ats_categories(df):

    if df.empty:

        return {

            "Excellent": 0,

            "Good": 0,

            "Average": 0,

            "Poor": 0
        }

    excellent = len(

        df[df["ats_score"] >= 85]

    )

    good = len(

        df[
            (df["ats_score"] >= 70)
            &
            (df["ats_score"] < 85)
        ]
    )

    average = len(

        df[
            (df["ats_score"] >= 50)
            &
            (df["ats_score"] < 70)
        ]
    )

    poor = len(

        df[df["ats_score"] < 50]

    )

    return {

        "Excellent": excellent,

        "Good": good,

        "Average": average,

        "Poor": poor

    }

df = get_resume_dataframe()

print(df.head())

print(overall_statistics(df))