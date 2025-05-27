import json
import os.path
import pathlib

from .parsers import ParseJobDesc, ParseResume
from .ReadPdf import read_single_pdf

READ_RESUME_FROM = "Data/Resumes/"
SAVE_DIRECTORY = "Data/Processed/Resumes"

class ResumeProcessorAPI:
    def __init__(self, input_file):
        self.input_file = input_file  # Store the full path directly

    def process(self) -> bool:
        """
        Original method for the existing app: returns bool and saves to JSON file.
        """
        try:
            resume_dict = self._read_resumes(self.input_file)  # Pass full path
            self._write_json_file(resume_dict)
            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def parse_to_dict(self):
        """
        New method for the API: returns the resume dictionary without saving to file.
        """
        try:
            resume_dict = self._read_resumes(self.input_file)  # Pass full path
            return resume_dict
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise  # Re-raise to be caught by the caller

    def _read_resumes(self, filepath):
        """
        Reads the resumes from the input file and parses them using ParseResume.
        """
        data = read_single_pdf(filepath)  # Use the full path directly
        output = ParseResume(data).get_JSON()
        return output

    def _read_job_desc(self, filepath):
        data = read_single_pdf(filepath)  # Use the full path directly
        output = ParseJobDesc(data).get_JSON()
        return output

    def _write_json_file(self, resume_dictionary):
        file_name = f"Resume-{os.path.basename(self.input_file)}{resume_dictionary['unique_id']}.json"
        save_directory_name = pathlib.Path(SAVE_DIRECTORY) / file_name
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)  # Ensure directory exists
        json_object = json.dumps(resume_dictionary, sort_keys=True, indent=4)
        with open(save_directory_name, "w+") as outfile:
            outfile.write(json_object)