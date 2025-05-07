from flask import Blueprint, request, jsonify
import os
import uuid
import shutil
import logging
from scripts import ResumeProcessor

api = Blueprint('resume_api', __name__)

# Temporary upload folder
UPLOAD_FOLDER = os.path.join("temp_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api.route("/parse_resume", methods=["POST"])
def parse_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    try:
        # Save file to temp location
        temp_filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(file_path)

        # Process resume
        processor = ResumeProcessor(file_path)
        success = processor.process()

        if not success:
            return jsonify({"error": "Resume processing failed"}), 500

        # Read the parsed JSON file
        json_filename = temp_filename.replace(".pdf", ".json")
        json_path = os.path.join("Data", "Processed", "Resumes", json_filename)

        if not os.path.exists(json_path):
            return jsonify({"error": "Parsed JSON not found"}), 500

        with open(json_path, "r") as f:
            parsed_data = f.read()

        return jsonify({"parsed_resume": parsed_data}), 200

    except Exception as e:
        logging.exception("Failed to parse resume")
        return jsonify({"error": str(e)}), 500
