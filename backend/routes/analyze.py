from flask import Blueprint, request, jsonify
from models.skill_matcher import SkillMatcher
from utils.parse_resume import extract_resume_text
import os

analyze = Blueprint('analyze', __name__)

@analyze.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        resume_text = ""
        job_description = ""

        # If a file is uploaded
        if 'resume' in request.files:
            resume_file = request.files['resume']
            temp_path = "tmp_resume_upload"
            resume_file.save(temp_path)

            # Extract text (PDF/DOCX/Image)
            try:
                resume_text = extract_resume_text(temp_path)
            except Exception as e:
                os.remove(temp_path)
                return jsonify({"error": f"Error extracting text: {str(e)}"}), 400

            os.remove(temp_path)
            job_description = request.form.get('job_description', '')

        else:
            # If data is sent as JSON
            data = request.get_json(force=True)
            resume_text = data.get('resume', '')
            job_description = data.get('job_description', '')

        # Skill matching logic
        skill_matcher = SkillMatcher()
        missing_skills = skill_matcher.get_missing_skills(resume_text, job_description)

        # Response logic
        if not missing_skills:
            response_message = "You already have the required skills for this job. Great work!"
        else:
            response_message = "Here are some skills you can improve or take courses on."

        return jsonify({
            'message': response_message,
            'missing_skills': missing_skills
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}"
        }), 500
