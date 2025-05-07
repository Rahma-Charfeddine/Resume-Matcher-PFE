from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename


from scripts.ResumeProcessor import ResumeProcessor


api = Blueprint('api', __name__)

# Example: Resume parsing API
@api.route("/parse_resume", methods=["POST"])
def parse_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join("Data", "Resumes", filename)
    file.save(file_path)

    try:
        processor = ResumeProcessor(file_path)
        processor.process()
        processed_path = os.path.join("Data", "Processed", "Resumes", filename.replace(".pdf", ".json"))
        with open(processed_path, "r") as f:
            parsed_json = f.read()
        return jsonify({"parsed_resume": parsed_json}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# You can add more APIs below
@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200
