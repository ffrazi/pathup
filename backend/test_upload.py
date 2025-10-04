import requests
from utils.ocr import ocr_image_to_text


# 🔹 Import your OCR function
# from your_ocr_module import extract_text_from_file
# Example:
# def extract_text_from_file(file_path):
#     # your OCR code
#     return extracted_text

file_path = r"D:\hope_project\PathUp\backend\test_files\sample_resume.pdf.pdf"

# 🔹 Provide a realistic job description
job_description = """
We are looking for a Machine Learning Engineer with skills in Python,
data analysis, business intelligence, and automation.
"""

# 🔹 Send the file and job description to your Flask API
url = "http://127.0.0.1:5000/analyze"
with open(file_path, "rb") as f:
    files = {"resume": f}
    data = {"job_description": job_description}
    response = requests.post(url, files=files, data=data)

print("Status:", response.status_code)
print("Response:")
print(response.text)
