import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate('firebase_service_account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

with open('../data/skills_mapping.json', 'r') as f:
    skill_map = json.load(f)

collection = db.collection('skills')

for skill, course in skill_map.items():
    collection.document(skill).set({'micro_course': course})

print("Uploaded all skills to Firestore!")
