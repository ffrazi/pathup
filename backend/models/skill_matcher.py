from sentence_transformers import SentenceTransformer, util
import spacy
import firebase_admin
from firebase_admin import credentials, firestore
import en_core_web_sm
import torch


# ✅ Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_service_account.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()


def fetch_micro_course(skill):
    """
    Fetch a micro-course recommendation from Firestore for a given skill.
    Each document in 'skills' collection should look like:
    { "micro_course": "Complete an online course on XYZ" }
    """
    try:
        doc = db.collection('skills').document(skill).get()
        if doc.exists:
            data = doc.to_dict()
            return data.get('micro_course', 'No micro-course available')
        return 'No micro-course available'
    except Exception as e:
        print(f"[Firebase Error] Could not fetch for skill '{skill}': {e}")
        return 'Error fetching micro-course'


class SkillMatcher:
    def __init__(self):
        # ✅ Load heavy models only once (not every request)
        if not hasattr(SkillMatcher, 'model_instance'):
            SkillMatcher.model_instance = SentenceTransformer('all-MiniLM-L6-v2')
        if not hasattr(SkillMatcher, 'nlp_instance'):
            SkillMatcher.nlp_instance = en_core_web_sm.load()

        self.model = SkillMatcher.model_instance
        self.nlp = SkillMatcher.nlp_instance


    def extract_keywords(self, text):
        """
        Extracts potential skill-like nouns/proper nouns from the input text.
        Example: 'project management' -> ['project', 'management']
        """
        if not text or not text.strip():
            return []
        doc = self.nlp(text)
        keywords = [token.text.strip() for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text.strip()) > 2]
        return list(set(keywords))  # unique only


    def match_skills(self, resume, job_description):
        """
        Finds which job-related skills are *missing* in the resume using semantic similarity.
        """
        resume_keywords = self.extract_keywords(resume)
        job_keywords = list(set(self.extract_keywords(job_description)))

        if not resume_keywords or not job_keywords:
            return []

        resume_emb = self.model.encode(resume_keywords, convert_to_tensor=True)
        job_emb = self.model.encode(job_keywords, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(job_emb, resume_emb)  # shape: (len(job_kw), len(resume_kw))
        threshold = 0.55  # tuned to reduce false positives

        missing = []
        for i, job_kw in enumerate(job_keywords):
            # If none of the resume keywords is semantically close
            if torch.max(similarity[i]).item() < threshold:
                missing.append(job_kw)
        return missing


    def get_missing_skills(self, resume, job_description):
        """
        For each missing skill, fetch a micro-course suggestion.
        """
        missing_skills = self.match_skills(resume, job_description)
        if not missing_skills:
            return []

        results = []
        for skill in missing_skills:
            course = fetch_micro_course(skill)
            results.append({
                "skill": skill,
                "micro_course": course
            })
        return results
