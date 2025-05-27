import json
import os.path
import pathlib # this module works with filesystem paths

from .parsers import ParseJobDesc, ParseResume # importing classes from the .parsers module
from .ReadPdf import read_single_pdf  #importing the read_single_pdf function from the .ReadPdf module
READ_JOB_DESCRIPTION_FROM = "Data/JobDescription/" #define a constant for the directory path to read job descriptions from
SAVE_DIRECTORY = "Data/Processed/JobDescription"  #define a constant for the directory path to save processed files


class JobDescriptionProcessorAPI:
    def __init__(self, input_file):
        """

            Initializes ann instance of JobDescrptionProcessor with input_file
            :param input_file: the path to the file containing the job descriptions
            Constructs inut_file_name by joining READ_JOB_DECRIPTION_FROM and input_file
            :return: None

        """
        self.input_file = input_file #initialize instance variable input_file with the input parameter
        #self.input_file_name = os.path.join(READ_JOB_DESCRIPTION_FROM + self.input_file) #construct full path to input file using os.path.join
        
        
        # i changed the following with the next expression


        #self.input_file_name = os.path.join(READ_JOB_DESCRIPTION_FROM + self.input_file)


        self.input_file_name = input_file
        #self.input_file_name=self.input_file
    
    def process(self) -> bool:
        """
            Tries to process the job description:
            calls _read_resumes() to read and parse resume data
            calls _write_jason_file() to save parsed resume data as JSON
            Returns True if successful, otherwise catches and prints any exceptions, returning False
        """
        try:
            # this first line of code is not correct (read_resume for job description )
            #resume_dict = self._read_resumes() #call _read_resumes() method to read and parse resume data
            
            # updated version:
            JD_dict = self._read_job_desc()


            
            self._write_json_file(JD_dict)  #call _write_json_file() method to save parsed resume data as JSON
            #saved_file_name= self._write_json_file(resume_dict)
            return True
            #return saved_file_name
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def _read_resumes(self) -> dict:

        data = read_single_pdf(self.input_file_name) #Read the pdf file specified by input_file_name
        output = ParseResume(data).get_JSON() #Parse data using ParseResume class and get JSON representation
        return output

    def _read_job_desc(self) -> dict:
        """
           Reads the job descriptions from the input file and parses them using ParseJobDesc returning the JSON representation
        """
        data = read_single_pdf(self.input_file_name)
        output = ParseJobDesc(data).get_JSON()
        return output

    def _write_json_file(self, resume_dictionary: dict):
        file_name = str(
            "JobDescription-"
            + self.input_file
            + resume_dictionary["unique_id"]
            + ".json"
        )
        save_directory_name = pathlib.Path(SAVE_DIRECTORY) / file_name
        json_object = json.dumps(resume_dictionary, sort_keys=True, indent=14)
        with open(save_directory_name, "w+") as outfile:
            outfile.write(json_object)

    def parse_to_dict(self):
        """
        New method for the API: returns the resume dictionary without saving to file.
        """
        try:
            JD_dict = self._read_job_desc()
            return JD_dict
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise  # Re-raise to be caught by the caller
