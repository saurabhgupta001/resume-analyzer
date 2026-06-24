

vectorizer = TfidfVectorizer()

def match_score(resume_text, job_description):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    docs = [resume_text, job_description]

    tfidf_matrix = vectorizer.fit_transform(docs)

    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return round(score[0][0] * 100, 2)