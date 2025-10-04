import pandas as pd
import json

df = pd.read_csv('resumes_development.csv')

# List a subset of skill columns for demonstration
skill_cols = df.columns[1:20].tolist()

# Create a simple skill-to-micro-course mapping
skill_map = {skill: f"Complete an online course on {skill}" for skill in skill_cols}

# Save to JSON
with open('skills_mapping.json', 'w') as f:
    json.dump(skill_map, f, indent=2)

df = pd.read_csv('resumes_pilot.csv')

# List a subset of skill columns for demonstration
skill_cols = df.columns[1:20].tolist()

# Create a simple skill-to-micro-course mapping
skill_map = {skill: f"Complete an online course on {skill}" for skill in skill_cols}

# Save to JSON
with open('job_description.json', 'w') as f:
    json.dump(skill_map, f, indent=2)