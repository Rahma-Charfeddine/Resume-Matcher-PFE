import re
import urllib.request

import spacy

from .utils import TextCleaner
import os
from groq import Groq

from prompt_templates.parsing_prompt import parse_keywords_prompt

# Load the English model
#nlp = spacy.load("en_core_web_sm")
# when i switched to the following it gave me a better parsing result
nlp = spacy.load("en_core_web_trf")

RESUME_SECTIONS = [
    "Contact Information",
    "Objective",
    "Summary",
    "Professional Summary"
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
    "Licenses",
    "Awards",
    "Honors",
    "Publications",
    "References",
    "Technical Skills",
    "Computer Skills",
    "Programming Languages",
    "Software Skills",
    "Soft Skills",
    "Language Skills",
    "Professional Skills",
    "Transferable Skills",
    "Work Experience",
    "Professional Experience",
    "Employment History",
    "Internship Experience",
    "Volunteer Experience",
    "Leadership Experience",
    "Research Experience",
    "Teaching Experience",
]


JD_SECTIONS = [
    "Job Title",
    "Position Title",
    "Job Summary",
    "Position Summary",
    "Company Overview",
    "About the Company",
    "About Us",
    "Who We Are",
    "Job Description",
    "Responsibilities",
    "Key Responsibilities",
    "Duties",
    "Tasks",
    "Job Duties",
    "What You’ll Do",
    "Your Role",
    "Position Responsibilities",
    "Required Skills",
    "Qualifications",
    "Requirements",
    "What We’re Looking For",
    "What You Bring",
    "Desired Qualifications",
    "Minimum Requirements",
    "Preferred Qualifications",
    "Skills and Experience",
    "Education",
    "Experience",
    "Technical Skills",
    "Soft Skills",
    "Perks",
    "Benefits",
    "What We Offer",
    "Nice to Have",
    "Location",
    "Employment Type",
    "Work Schedule",
    "Travel Requirements",
    "Equal Opportunity Employer",
    "How to Apply"
]


RELEVANT_JD_SECTIONS = [
    "Job Description",
    "Responsibilities",
    "Requirements",
    "Skills",
    "Key Responsibilities",
    "Required Skills",
    "Preferred Skills",
    "Technical Skills",
    "Desired Qualifications",
    "Qualifications",
    "What You’ll Do",
    "What You Bring"
]

IRRELEVANT_JD_SECTIONS = [
    "About Us",
    "Who We Are",
    "Company Overview",
    "Benefits",
    "What We Offer",
    "How to Apply",
    "Equal Opportunity Employer"
]



class DataExtractor:
    """
    A class for extracting various types of data from text.
    """

    def __init__(self, raw_text: str):
        """
        Initialize the DataExtractor object.

        Args:
            raw_text (str): The raw input text.
        """

        self.text = raw_text
        self.clean_text = TextCleaner.clean_text(self.text)
        
        self.doc = nlp(self.clean_text)




        '''
        self.abbreviation_dict = {
            "CTO": "Chief Technology Officer",
            "CIO": "Chief Information Officer",
            "CISO": "Chief Information Security Officer",
            "VP": "Vice President",
            "PM": "Project Manager / Product Manager",
            "BA": "Business Analyst",
            "QA": "Quality Assurance",
            "SDE": "Software Development Engineer",
            "SW": "Software Engineer",
            "DEV": "Developer",
            "ENG": "Engineer",
            "UI": "User Interface Designer",
            "UX": "User Experience Designer",
            "DBA": "Database Administrator",
            "SysAdmin": "System Administrator",
            "IT": "Information Technology",
            "DevOps": "Development and Operations",
            "ML": "Machine Learning",
            "AI": "Artificial Intelligence",
            "BI": "Business Intelligence",
            "DS": "Data Scientist",
            "DA": "Data Analyst",
            "DWH": "Data Warehouse",
            "NLP": "Natural Language Processing",
            "IoT": "Internet of Things",
            "VR": "Virtual Reality",
            "AR": "Augmented Reality",
            "KPI": "Key Performance Indicator",
            "API": "Application Programming Interface",
            "SDK": "Software Development Kit",
            "HTML": "HyperText Markup Language",
            "CSS": "Cascading Style Sheets",
            "JS": "JavaScript",
            "SQL": "Structured Query Language",
            "NoSQL": "Not Only SQL"
        }
        '''



    def extract_links(self):
        """
        Find links of any type in a given string.

        Args:
            text (str): The string to search for links.

        Returns:
            list: A list containing all the found links.
        """
        link_pattern = r"\b(?:https?://|www\.)\S+\b"
        links = re.findall(link_pattern, self.text)
        return links
    





    def extract_links_extended(self):
        """
        Extract links of all kinds (HTTP, HTTPS, FTP, email, www.linkedin.com,
          and github.com/user_name) from a webpage.

        Args:
            url (str): The URL of the webpage.

        Returns:
            list: A list containing all the extracted links.
        """
        links = []
        try:
            response = urllib.request.urlopen(self.text)
            html_content = response.read().decode("utf-8")
            pattern = r'href=[\'"]?([^\'" >]+)'
            raw_links = re.findall(pattern, html_content)
            for link in raw_links:
                if link.startswith(
                    (
                        "http://",
                        "https://",
                        "ftp://",
                        "mailto:",
                        "www.linkedin.com",
                        "github.com/",
                        "twitter.com",
                    )
                ):
                    links.append(link)
        except Exception as e:
            print(f"Error extracting links: {str(e)}")
        return links
    





    def extract_names(self):
        """Extracts and returns a list of names from the given
        text using spaCy's named entity recognition.

        Args:
            text (str): The text to extract names from.

        Returns:
            list: A list of strings representing the names extracted from the text.
        """
        names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        return names
    



    def extract_emails(self):
        """
        Extract email addresses from a given string.

        Args:
            text (str): The string from which to extract email addresses.

        Returns:
            list: A list containing all the extracted email addresses.
        """
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        emails = re.findall(email_pattern, self.text)
        return emails
    



    def extract_phone_numbers(self):
        """
        Extract phone numbers from a given string.

        Args:
            text (str): The string from which to extract phone numbers.

        Returns:
            list: A list containing all the extracted phone numbers.
        """
        phone_number_pattern = (
            r"^(\+\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        )
        phone_numbers = re.findall(phone_number_pattern, self.text)
        return phone_numbers
    


    def extract_experience(self):
        """
        Extract experience from a given string. It does so by using the Spacy module.

        Args:
            text (str): The string from which to extract experience.

        Returns:
            str: A string containing all the extracted experience.
        """
        experience_section = []
        in_experience_section = False

        for token in self.doc:
            if token.text in RESUME_SECTIONS:
                if token.text == "Experience" or "EXPERIENCE" or "experience":
                    in_experience_section = True
                else:
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(token.text)

        return " ".join(experience_section)
    


    def extract_position_year(self):
        """
        Extract position and year from a given string.

        Args:
            text (str): The string from which to extract position and year.

        Returns:
            list: A list containing the extracted position and year.
        """
        position_year_search_pattern = (
            r"(\b\w+\b\s+\b\w+\b),\s+(\d{4})\s*-\s*(\d{4}|\bpresent\b)"
        )
        position_year = re.findall(position_year_search_pattern, self.text)
        return position_year
    
    '''
    def extract_from_abbreviations(self):
                import spacy

        # Load spaCy model
        nlp = spacy.load("en_core_web_sm")

        def expand_with_spacy(text):
            doc = nlp(text)
            expanded_text = []
            
            for token in doc:
                if token.ent_type_ in ["ORG", "GPE", "PRODUCT"]:  # Adjust based on entity types
                    expanded_text.append(token._.long_form if token._.long_form else token.text)
                else:
                    expanded_text.append(token.text)
            
            return " ".join(expanded_text)

        resume_text = "Experience in AI, ML, and NLP for Big Data applications."
        print(expand_with_spacy(resume_text))


''' 

    def extract_from_abbreviations(self):
            """
            Replace abbreviations in the text with their full names.

            Returns:
                str: The modified text with abbreviations expanded.
            """
            modified_text = self.clean_text
            for abbreviation, full_name in self.abbreviation_dict.items():
                # Use regex to replace abbreviations while preserving case
                modified_text = re.sub(rf'\b{abbreviation}\b', full_name, modified_text)
           
     
    ###### original version of extract_particular_words ########
    '''
    def extract_particular_words(self):
        """
        Extract nouns and proper nouns from the given text.

        Args:
            text (str): The input text to extract nouns from.

        Returns:
            list: A list of extracted nouns.
        """
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        nouns = [token.text for token in self.doc if token.pos_ in pos_tags]
        return nouns
    '''

    ###### modified version 1 ########
    #### of extract_particular_words #############
    '''
    def extract_particular_words(self):
        """
        Extract nouns and proper nouns from the given text.

        Args:
            text (str): The input text to extract nouns from.

        Returns:
            list: A list of extracted nouns.
        """
        pos_tags = ["NOUN", "PROPN", "ADJ"]  # Nouns, Proper Nouns, and Adjectives
        keyword_frequency = {}

        for token in self.doc:
            if token.pos_ in pos_tags:
                # Normalize the token text to lower case for consistency
                keyword = token.text.lower()
                if keyword in keyword_frequency:
                    keyword_frequency[keyword] += 1
                else:
                    keyword_frequency[keyword] = 1

        # Sort keywords by frequency in descending order
        sorted_keywords = dict(sorted(keyword_frequency.items(), key=lambda item: item[1], reverse=True))

        return sorted_keywords
    '''
    ###### modified version 2 ########
    #### of extract_particular_words #############
    '''
    def extract_particular_words(self):
        normalized_sections = {section.lower() for section in RESUME_SECTIONS}

        #named_entities = {ent.text.lower() for ent in self.doc.ents}
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}
        #nouns = [token.text for token in self.doc if token.pos_ in pos_tags and token.text.lower() not in normalized_sections and token.text.lower() not in named_entities ]
        
        excluded_token_ids = set()
        for ent in self.doc.ents:
             if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))


        nouns = [token.text for token in self.doc if token.pos_ in pos_tags 
                 and token.text.lower() not in normalized_sections 
                 #and token.ent_type_ not in ["PERSON", "ORG", "GPE"] 
                 and  not any(ent.label_ in excluded_ents and token.i >= ent.start and token.i < ent.end for ent in self.doc.ents)
                 and not any(bad in token.text.lower() for bad in blacklist_keywords)
                 and token.i not in excluded_token_ids]
        return nouns
        '''
    
    
    def extract_particular_words(self):
        normalized_sections = {section.lower() for section in RESUME_SECTIONS}
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        # Collect token indices to exclude
        excluded_token_ids = set()
        for ent in self.doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))

        # Final keyword extraction
        keywords = [
            token.text for token in self.doc
            if token.pos_ in pos_tags
            and token.text.lower() not in normalized_sections
            and token.i not in excluded_token_ids
            and not any(bad in token.text.lower() for bad in blacklist_keywords)
        ]

        return keywords
    


    def extract_particular_words_from_jd(self):
        """
        Extract meaningful words (nouns, proper nouns, adjectives) from the job description,
        even if there are no formal section headers.
        """
        # Step 1: Use full clean text since there's no clear sectioning
        jd_text = self.clean_text
        
        # Step 2: Process the text with spaCy
        doc = nlp(jd_text)
        
        # Step 3: Define what to include and exclude
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        # Step 4: Exclude named entities like company names, locations, etc.
        excluded_token_ids = set()
        for ent in doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))
        
        # Step 5: Extract keywords
        keywords = [
            token.text.lower() for token in doc
            if token.pos_ in pos_tags
            and token.i not in excluded_token_ids
            and token.text.lower() not in blacklist_keywords
            and len(token.text) > 2
        ]
        
        return list(set(keywords))  # Remove duplicates


    def extract_particular_words_from_jd_latest_22(self):
        import re

        # Step 1: Normalize section names
        irrelevant_sections = {s.lower() for s in IRRELEVANT_JD_SECTIONS}
        relevant_sections = {s.lower() for s in RELEVANT_JD_SECTIONS}
        all_sections = {s.lower(): s for s in JD_SECTIONS}

        # Step 2: Split text into sections using section headers
        section_pattern = re.compile(
            r"(?i)(" + "|".join(re.escape(s) for s in all_sections.values()) + r")"
        )

        parts = section_pattern.split(self.clean_text)
        sections = {}
        current_section = None

        for part in parts:
            part_clean = part.strip()
            part_lower = part_clean.lower()
            if part_lower in all_sections:
                current_section = part_lower
                sections[current_section] = ""
            elif current_section:
                sections[current_section] += " " + part_clean

        # Step 3: Keep only relevant sections
        filtered_text = " ".join(
            content for section, content in sections.items()
            if section not in irrelevant_sections
        )

        # Step 4: NLP processing
        doc = nlp(filtered_text)
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        # Remove named entities
        excluded_token_ids = set()
        for ent in doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))

        # Step 5: Extract keywords (similar to resume)
        keywords = [
            token.text for token in doc
            if token.pos_ in pos_tags
            and token.text.lower() not in all_sections  # remove section headers as keywords
            and token.i not in excluded_token_ids
            and not any(bad in token.text.lower() for bad in blacklist_keywords)
        ]

        return keywords


    def extract_particular_words_from_JD_original(self):
        normalized_sections = {section.lower() for section in JD_SECTIONS }
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        # Collect token indices to exclude
        excluded_token_ids = set()
        for ent in self.doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))

        # Final keyword extraction
        keywords = [
            token.text for token in self.doc
            if token.pos_ in pos_tags
            and token.text.lower() not in normalized_sections
            and token.i not in excluded_token_ids
            and not any(bad in token.text.lower() for bad in blacklist_keywords)
        ]

        return keywords

    
    
    



 
    




    def extract_entities(self):
        """
        Extract named entities of types 'GPE' (geopolitical entity) and 'ORG' (organization) from the given text.

        Args:
            text (str): The input text to extract entities from.

        Returns:
            list: A list of extracted entities.
        """
        entity_labels = ["GPE", "ORG"]
        entities = [
            token.text for token in self.doc.ents if token.label_ in entity_labels
        ]
        return list(set(entities))
    

    def extract_keywords_ai_ex(self):
        """
        Uses an AI model to extract categorized keywords from the text (resume or JD).

        Returns:
            dict: A JSON-style dictionary of extracted keywords grouped by type.
        """
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            prompt = parse_keywords_prompt.format(content=self.clean_text)

            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            result = ""
            for chunk in completion:
                result += chunk.choices[0].delta.content or ""

            import json
            return json.loads(result.strip())

        except Exception as e:
            print(f"AI keyword extraction failed: {str(e)}")
            return {}


    def extract_keywords_ai(self):
        """
        Uses an AI model to extract categorized keywords from the text (resume or JD).

        Returns:
            dict: A JSON-style dictionary of extracted keywords grouped by type.
        """
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = parse_keywords_prompt.format(content=self.clean_text)

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                     "content": prompt
                }
            ],
            temperature=0.3,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        result = ""
        for chunk in completion:
            result += chunk.choices[0].delta.content or ""

        return result.strip()

     

    def get_resume_sections(self):
        
        text = self.text.lower()
        experience_pattern = r"(work experience|professional experience|employment history|experience)"
        skills_pattern = r"(skills|technical skills|core competencies|technologies)"

        sections = {"experience": "", "skills": ""}

        # Split based on common section titles
        exp_match = re.search(experience_pattern, text)
        skill_match = re.search(skills_pattern, text)

        if exp_match:
            exp_start = exp_match.start()
            sections["experience"] = text[exp_start:]
            if skill_match:
                sections["experience"] = text[exp_start:skill_match.start()]

        if skill_match:
            skill_start = skill_match.start()
            sections["skills"] = text[skill_start:]
        

        print (sections)

        return sections