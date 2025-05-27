import json
import os
import os.path
import pathlib

from scripts.Extractor import DataExtractor
from scripts.KeytermsExtraction import KeytermExtractor
from scripts.utils.Utils import CountFrequency, TextCleaner, generate_unique_id

SAVE_DIRECTORY = "../../Data/Processed/Resumes"


class ParseResume:

    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextCleaner.clean_text(self.resume_data)
        
        #self.clean_data = TextCleaner(self.resume_data).clean_text()

        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.name = DataExtractor(self.clean_data[:30]).extract_names()
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.emails = DataExtractor(self.resume_data).extract_emails()
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        self.years = DataExtractor(self.clean_data).extract_position_year()
        


        # key_words 
        # classical method
        #self.key_words = DataExtractor(self.clean_data).extract_particular_words()

        #calling AI parsing for key_words
        self.key_words = DataExtractor(self.clean_data).extract_keywords_ai()





        self.pos_frequencies = CountFrequency(self.clean_data).count_frequency()



        # uses on sgrank
        #self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()



        #uses new method
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank_newest()


        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()
        






        #self.skills_section = DataExtractor(self.clean_data).extract_skills_section_from_cv()



        # sections seperated 




        self.name_section= DataExtractor(self.resume_data).extract_name_section()
        self.phone_section =DataExtractor(self.resume_data).extract_phone_section()
        self.location_section =DataExtractor(self.resume_data).extract_location_section()
        self.email_section =DataExtractor(self.resume_data).extract_email_section()



        self.social_links_section= DataExtractor(self.resume_data).extract_social_links()



        #self.experience_section =DataExtractor(self.resume_data).extract_experience_section()
        
        #self.skills_section = DataExtractor(self.resume_data).extract_skills_section()
        
        
        

        self.education_section = DataExtractor(self.resume_data).extract_education_ai()
        self.skills_section = DataExtractor(self.resume_data).extract_skills_ai()
        self.experience_section =DataExtractor(self.resume_data).extract_experience_ai()




    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "unique_id": generate_unique_id(),
            #"resume_data": self.resume_data,
            #"clean_data": self.clean_data,
            #"entities": self.entities,
            "extracted_keywords": self.key_words,
            #"keyterms": self.keyterms,
            #"name": self.name,
            #"experience": self.experience,
            #"emails": self.emails,
            #"phones": self.phones,
            #"years": self.years,
            #"bi_grams": str(self.bi_grams),
            #"tri_grams": str(self.tri_grams),
            #"pos_frequencies": self.pos_frequencies,

            
# profile page sections    

            "name_section":self.name_section,
            "phone_section": self.phone_section ,
            "location_section":self.location_section ,
            "email_section": self.email_section,


            "social_media_section": self.social_links_section,
            "experience_section": self.experience_section,


            "skills_section": self.skills_section,
            "education_section": self.education_section,



        

        }
        
      

    
        return resume_dictionary
