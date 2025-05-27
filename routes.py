









# resume parsing working in this version 



'''
from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from scripts.ResumeProcessorAPI import ResumeProcessorAPI
from scripts.JobDescriptionProcessorAPI import JobDescriptionProcessorAPI



api = Blueprint('api', __name__)

# Define upload folder and allowed extensions
UPLOAD_FOLDER = "Data/Resumes/"
UPLOAD_FOLDER_JDS = "Data/JobDescription/"
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_JDS, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/parse_resume', methods=['POST'])
def parse_resume():
    print("request.files:", request.files)
    print("request.form:", request.form)
    print("request.content_type:", request.content_type)

    # Check if a file was uploaded
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part in the request"}), 400

    file = request.files['resume']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Validate file extension
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Sanitize the filename and save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    # Process the file
    try:
        processor = ResumeProcessorAPI(filepath)  # Pass full path to ResumeProcessor
        resume_dict = processor.parse_to_dict()  # Use the new method
    except Exception as e:
        # Clean up the file even if processing fails
        try:
            os.remove(filepath)
        except Exception:
            pass
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    # Clean up the file after successful processing
#    try:
#        os.remove(filepath)
#    except Exception as e:
#        print(f"Warning: Failed to delete file {filepath}: {str(e)}")

    # Return the parsed resume as JSON
    return jsonify({"parsed_resume": resume_dict}), 200










# api for job description parsing
@api.route('/parse_job_description', methods=['POST'])
def parse_job_description():
    """
    API endpoint to parse a job description PDF file and return the extracted data as JSON.
    
    Returns:
        JSON response with the parsed job description data or an error message.
    """
    print("request.files:", request.files)
    print("request.form:", request.form)
    print("request.content_type:", request.content_type)

    # Check if a file was uploaded
    if 'job_description' not in request.files:
        return jsonify({"error": "No job description file part in the request"}), 400

    file = request.files['job_description']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Validate file extension
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Sanitize the filename and save the file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER_JDS, filename)

    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    # Process the file
    try:
        processor = JobDescriptionProcessorAPI(filepath)  # Pass full path to JobDescriptionProcessor
        jd_dict = processor.parse_to_dict()  # Use the parse method
    except Exception as e:
        # Clean up the file even if processing fails
        try:
            os.remove(filepath)
        except Exception:
            pass
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    # Clean up the file after successful processing
    #try:
    #    os.remove(filepath)
    #except Exception as e:
    #    print(f"Warning: Failed to delete file {filepath}: {str(e)}")

    # Return the parsed job description as JSON
    return jsonify({"parsed_job_description": jd_dict}), 200

    '''

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from scripts.ResumeProcessorAPI import ResumeProcessorAPI
from scripts.JobDescriptionProcessorAPI import JobDescriptionProcessorAPI
from scripts.similarity.get_score import *

api = Blueprint('api', __name__)

# Define upload folder and allowed extensions
UPLOAD_FOLDER = "Data/Resumes/"
UPLOAD_FOLDER_JDS = "Data/JobDescription/"  # Correct folder name
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_JDS, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/parse_resume', methods=['POST'])
def parse_resume():
    print("request.files:", request.files)
    print("request.form:", request.form)
    print("request.content_type:", request.content_type)

    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part in the request"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Saving file to: {filepath}")

    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        print(f"Processing file: {filepath}")
        processor = ResumeProcessorAPI(filepath)
        resume_dict = processor.parse_to_dict()
    except Exception as e:
        try:
            os.remove(filepath)
        except Exception:
            pass
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    # try:
    #     os.remove(filepath)
    # except Exception as e:
    #     print(f"Warning: Failed to delete file {filepath}: {str(e)}")

    return jsonify({"parsed_resume": resume_dict}), 200

@api.route('/parse_job_description', methods=['POST'])
def parse_job_description():
    """
    API endpoint to parse a job description PDF file and return the extracted data as JSON.
    
    Returns:
        JSON response with the parsed job description data or an error message.
    """
    print("request.files:", request.files)
    print("request.form:", request.form)
    print("request.content_type:", request.content_type)

    if 'job_description' not in request.files:
        return jsonify({"error": "No job description file part in the request"}), 400

    file = request.files['job_description']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER_JDS, filename)
    print(f"Saving file to: {filepath}")

    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        print(f"Processing file: {filepath}")
        processor = JobDescriptionProcessorAPI(filepath)
        jd_dict = processor.parse_to_dict()
    except Exception as e:
        try:
            os.remove(filepath)
        except Exception:
            pass
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

    # try:
    #    os.remove(filepath)
    # except Exception as e:
    #    print(f"Warning: Failed to delete file {filepath}: {str(e)}")

    return jsonify({"parsed_job_description": jd_dict}), 200









@api.route('/calculate_compatibility', methods=['POST'])
def calculate_compatibility():
    """
    API endpoint to calculate the compatibility score between a resume and a job description
    using extracted keywords and an AI-based scoring method.

    Returns:
        JSON response with the compatibility score.
    """
    print("request.files:", request.files)
    print("request.form:", request.form)
    print("request.content_type:", request.content_type)

    # Check if both files are provided
    if 'resume' not in request.files or 'job_description' not in request.files:
        return jsonify({"error": "Both resume and job description files are required"}), 400

    resume_file = request.files['resume']
    jd_file = request.files['job_description']

    # Check if files were selected
    if resume_file.filename == '':
        return jsonify({"error": "No resume file selected"}), 400
    if jd_file.filename == '':
        return jsonify({"error": "No job description file selected"}), 400

    # Validate file extensions
    if not allowed_file(resume_file.filename):
        return jsonify({"error": "Resume file type not allowed"}), 400
    if not allowed_file(jd_file.filename):
        return jsonify({"error": "Job description file type not allowed"}), 400



    base_url = "http://127.0.0.1:5000/api"


    # Sanitize filenames and save files temporarily
    resume_filename = secure_filename(resume_file.filename)
    jd_filename = secure_filename(jd_file.filename)
    resume_filepath = os.path.join(UPLOAD_FOLDER, resume_filename)
    jd_filepath = os.path.join(UPLOAD_FOLDER_JDS, jd_filename)
    print(f"Saving resume to: {resume_filepath}")
    print(f"Saving job description to: {jd_filepath}")

    # Save the files
    try:
        resume_file.save(resume_filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save resume file: {str(e)}"}), 500

    try:
        jd_file.save(jd_filepath)
    except Exception as e:
        try:
            os.remove(resume_filepath)  # Clean up resume file if JD save fails
        except Exception:
            pass
        return jsonify({"error": f"Failed to save job description file: {str(e)}"}), 500

    # Process both files
    try:
        print(f"Processing resume: {resume_filepath}")
        resume_processor = ResumeProcessorAPI(resume_filepath)
        resume_dict = resume_processor.parse_to_dict()
        resume_keywords = resume_dict.get("extracted_keywords", [])

        print(f"Processing job description: {jd_filepath}")
        jd_processor = JobDescriptionProcessorAPI(jd_filepath)
        jd_dict = jd_processor.parse_to_dict()
        jd_keywords = jd_dict.get("extracted_keywords", [])
    except Exception as e:
        # Clean up both files if processing fails
        try:
            os.remove(resume_filepath)
            os.remove(jd_filepath)
        except Exception:
            pass
        return jsonify({"error": f"Failed to process files: {str(e)}"}), 500

    # Clean up files after processing (commented out for now)
    # try:
    #     os.remove(resume_filepath)
    #     os.remove(jd_filepath)
    # except Exception as e:
    #     print(f"Warning: Failed to delete files - Resume: {resume_filepath}, JD: {jd_filepath}: {str(e)}")

    # Calculate compatibility score using the get_score method
    if not resume_keywords or not jd_keywords:
        return jsonify({"error": "No keywords extracted from resume or job description"}), 400

    resume_keywords_str = " ".join(resume_keywords)
    jd_keywords_str = " ".join(jd_keywords)
    compatibility_score = get_score(resume_keywords_str, jd_keywords_str)

    # Ensure the score is a valid number
    try:
        score = float(compatibility_score.strip())
        if not 0 <= score <= 100:
            raise ValueError("Score out of range (0-100)")
    except ValueError as e:
        return jsonify({"error": f"Invalid score value: {str(e)}"}), 500

    return jsonify({
        "compatibility score between Resume and Job Description": score
    }), 200