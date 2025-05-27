import re
import urllib.request
#from spacy.matcher import Matcher
import json
import spacy
from .utils import TextCleaner
import os
from groq import Groq
from prompt_templates.parsing_prompt import parse_keywords_prompt
from prompt_templates.experience_extractor_prompt import experience_extractor_prompt
from prompt_templates.skills_extractor_prompt import skills_extractor_prompt
from prompt_templates.education_extractor_prompt import education_extractor_prompt

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
        #self.textup= nlp(self.text)
        self.raw_doc= nlp(self.text)

        self.clean_text = TextCleaner.clean_text(self.text)
        
        self.doc = nlp(self.clean_text)



        self.sections = self._map_sections()








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
        
        jd_text = self.clean_text
        
        
        doc = nlp(jd_text)
        
      
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        
        excluded_token_ids = set()
        for ent in doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))
        
        
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

        #  Normalize section names
        irrelevant_sections = {s.lower() for s in IRRELEVANT_JD_SECTIONS}
        relevant_sections = {s.lower() for s in RELEVANT_JD_SECTIONS}
        all_sections = {s.lower(): s for s in JD_SECTIONS}

        #split text into sections using section headers
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

        #keep only relevant sections
        filtered_text = " ".join(
            content for section, content in sections.items()
            if section not in irrelevant_sections
        )

        # NLP processing
        doc = nlp(filtered_text)
        pos_tags = ["NOUN", "PROPN", "ADJ"]
        blacklist_keywords = {"linkedin", "github", "gitlab", "portfolio", "http", "https", "www"}
        excluded_ents = {"PERSON", "ORG", "GPE"}

        #remove named entities
        excluded_token_ids = set()
        for ent in doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))

        #Extract keywords
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
    





    def extract_keywords_ai_ex_version1(self):
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












# currently working 

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

        #return result.strip()
        keywords = [keyword.strip() for keyword in result.split('\n') if keyword.strip()]
        return keywords

     


    




    def get_all_resume_sections_V2(self):
        """
        Extract experience and skills sections from resume text.
        Combines all occurrences of skill-related sections.
        """
        text = self.text.lower()
        experience_pattern = r"(work experience|professional experience|employment history|experience)"
        skills_patterns = r"(skills|technical skills|core competencies|technologies|computer skills|programming languages|professional skills)"
        all_sections_pattern = r"(education|experience|work experience|professional experience|employment history|projects|certifications|languages|hobbies|interests|contact|summary|objective)"

        sections = {"experience": "", "skills": ""}

        # Extract experience section
        exp_match = re.search(experience_pattern, text)
        if exp_match:
            exp_start = exp_match.start()
            next_section = re.search(all_sections_pattern, text[exp_start + 10:])
            if next_section:
                exp_end = exp_start + 10 + next_section.start()
                sections["experience"] = text[exp_start:exp_end]
            else:
                sections["experience"] = text[exp_start:]

        # Extract all skill-related sections
        skills_matches = list(re.finditer(skills_patterns, text))
        skill_sections = []

        for idx, match in enumerate(skills_matches):
            skill_start = match.start()
            next_match = None

            # Try to find the next general section to know where this one ends
            next_section = re.search(all_sections_pattern, text[skill_start + 10:])
            if next_section:
                skill_end = skill_start + 10 + next_section.start()
                skill_sections.append(text[skill_start:skill_end])
            else:
                skill_sections.append(text[skill_start:])

        # Combine all skill sections
        sections["skills"] = "\n".join(skill_sections)

        return sections
    



    def extract_skills_section_from_cv_old(self):
        """
        Extracts only the skills-related content from the resume text.
        """
        text = self.text.lower()
        skills_patterns = r"(skills|technical skills|core competencies|technologies|computer skills|programming languages|professional skills)"
        all_sections_pattern = r"(education|experience|work experience|professional experience|employment history|projects|certifications|languages|hobbies|interests|contact|summary|objective)"

        skills_matches = list(re.finditer(skills_patterns, text))
        skill_sections = []

        for idx, match in enumerate(skills_matches):
            skill_start = match.start()
            next_section = re.search(all_sections_pattern, text[skill_start + 10:])
            if next_section:
                skill_end = skill_start + 10 + next_section.start()
                skill_sections.append(text[skill_start:skill_end])
            else:
                skill_sections.append(text[skill_start:])

        return "\n".join(skill_sections)

    

    

    



    

    
    
    




    



 



    def extract_all_names_section(self):
        doc = self.raw_doc
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names = ent.text.split()
                return names[0], names[-1] if len(names) > 1 else ("", "")
        return "", ""
    

#name
    #currently working
    def extract_name_section(self) -> dict[str, str]:
        """
        Extracts first and last names from raw text in a frontend-friendly format.
        
        Returns:
            {
                "First Name": "John",  # (or "" if not found)
                "Last Name": "Doe"     # (or "" if not found)
            }
        """
        doc = nlp(self.text)  # Process raw text
        
        #get all PERSON entities
        names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        
        if not names:
            return {"First Name": "", "Last Name": ""}
        
        #take the first detected name (most likely the candidate's name)
        full_name = names[0]
        name_parts = full_name.split()
        
        # extract first and last names
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        return {
            "First Name": first_name,
            "Last Name": last_name
        }





# email
    #currently working
    def extract_email_section(self) -> str:
        """
        Extracts the first valid email from raw text.
        Handles:
        - Standard formats (user@example.com)
        - Subdomains (user@sub.example.com)
        - Special chars in local part (user.name+tag@example.com)
        - New TLDs (user@example.photography)

        Returns:
            str: The first valid email found, or empty string if none.
        """
        #robust regex (RFC 5322 compliant subset)
        email_regex = r"""
            \b[a-zA-Z0-9._%+-]+    # Local part (user.name+tag)
            @                      # Literal @
            [a-zA-Z0-9.-]+         # Domain (subdomain.example)
            \.[a-zA-Z]{2,}\b       # TLD (.com, .photography, etc.)
        """
        match = re.search(email_regex, self.text, re.VERBOSE)
        return match.group(0) if match else ""


# loaction, address
    #currently working
    def extract_location_section(self):
        """
        Extracts location information exactly as it appears in the text.
        Returns the first found location string or empty string if none found.
        """
        doc = nlp(self.text)
        
        #look for these common location indicators
        location_keywords = [
            'address', 'location', 'based in', 'located in', 
            'residing in', 'from', 'current city', 'city'
        ]
        
        # check named entities
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                return ent.text
        
        # Then check for keywords followed by potential locations
        for i, token in enumerate(doc):
            if token.text.lower() in location_keywords and i+1 < len(doc):
                # Return the next 1-3 words as potential location
                return ' '.join(t.text for t in doc[i+1:i+4]).strip(' ,;')
        
           #looking for standalone location patterns
        for chunk in doc.noun_chunks:
            text = chunk.text.strip()
            if (any(c.isupper() for c in text) and 
                not any(t.like_email or t.like_url for t in chunk)):
                return text
        
        return ""




# phone number
    
    #currently working
    def extract_phone_section(self):
        """
        Extracts phone numbers from resume text, handling various international formats.
        Returns the first found phone number or empty string if none found.
        """
        # phone number regex pattern
        phone_pattern = re.compile(
            r'(?:\+?\d{1,3}[-.\s]?)?'  # Optional country code
            r'\(?\d{3}\)?[-.\s]?'      # Area code with optional parentheses
            r'\d{3}[-.\s]?\d{4}'       # Phone number part
            r'(?:\s*(?:#|x|ext|extension)\s*\d+)?'  # Optional extension
        )
        
        # find  matches in the text
        matches = phone_pattern.finditer(self.text)
        
        for match in matches:
            # get the matched phone number
            phone_number = match.group()
            
            # basic validation - should contain at least 10 digits
            if sum(c.isdigit() for c in phone_number) >= 10:
                return phone_number.strip()
        
        return ""



  




 # Skills       
    #old not  working
    def extract_skills_sectionV1(self) -> list:
        #match the Skills section content
        pattern = re.compile(r"Skills\s*[:\-]?\s*(.*?)(?=\n[A-Z][a-z]+|\Z)", re.DOTALL | re.IGNORECASE)
        match = pattern.search(self.text)
        

        if match:
            skills_text = match.group(1)

            # split by newlines or commas, then strip each skill
            raw_skills = re.split(r"[\n,•\u2022]", skills_text)
            
            # clean and keep only meaningful skill strings
            skills = [skill.strip() for skill in raw_skills if len(skill.strip()) > 1]
            return skills
        
        

        return []
    
 # Skills       
    #currently working
    def extract_skills_sectionV2(self) -> list:
        """
        Extract the Skills section from the CV text.

        Returns:
            list: A list of skills extracted from the Skills section.
        """
        # Match the Skills section as a standalone section header
        pattern = re.compile(
            r"(?:\n|^)(Skills|Core Competencies|Technical Skills|Key Skills|Professional Skills|Programming Skills|Technical Skills|Tech Stack)\s*[:\-]?\s*\n(.*?)(?=\n{2,}|\n(?:Experience|Education|Work History|Projects|Certifications|[A-Z][a-zA-Z]*\s*[:\-])|\Z)",
            re.DOTALL | re.IGNORECASE
        )
        match = pattern.search(self.text)

        if match:
            skills_text = match.group(2).strip()  # Group 2 contains the skills content
            print(f"Extracted skills text: {skills_text}")  # Debug print

            # Replace newlines with commas to normalize the list
            skills_text = re.sub(r"\n\s*", ", ", skills_text)

            # Split on commas, handling spaces after commas
            raw_skills = re.split(r",\s*", skills_text)

            # Clean each skill: remove trailing punctuation and filter out short/empty entries
            skills = [
                re.sub(r"[.,;]$", "", skill.strip())
                for skill in raw_skills
                if len(skill.strip()) > 1 and skill.strip()
            ]
            print(f"Parsed skills: {skills}")  # Debug print

            return skills

        print("No Skills section found.")  # Debug print
        return []

# social media links:
    #currently working
   
    def extract_social_links(self):
        """
        Simple but effective social link extractor using direct string matching
        """
        # list of platform domains to look for
        PLATFORMS = {
            'linkedin': ['linkedin.com/in/', 'linkedin.com/company/'],
            'github': ['github.com/'],
            'gitlab': ['gitlab.com/'],
            'stackoverflow': ['stackoverflow.com/users/'],
            'kaggle': ['kaggle.com/'],
            'leetcode': ['leetcode.com/'],
            'medium': ['medium.com/', 'medium.com/@'],
            'bitbucket': ['bitbucket.org/'],
            'hackerrank': ['hackerrank.com/'],
            'twitter': ['twitter.com/'],
            'facebook': ['facebook.com/'],
            'instagram': ['instagram.com/']
        }
        





        #additional common patterns that might indicate a portfolio
        PORTFOLIO_KEYWORDS = ['portfolio', 'website', 'personal site', 'visit:']
        
        found_links = {}
        
        # split text into words while preserving URLs
        words = re.split(r'[\s,;()]', self.text)
        
        for word in words:
            #skip empty words and obvious non-URLs
            if not word or '.' not in word or '@' in word:
                continue
                
            # skip common false positives
            if any(x in word.lower() for x in ['mailto:', '.png', '.jpg', '.pdf']):
                continue
                
            # normalize the word (remove trailing punctuation)
            clean_word = word.strip('.,:;!?"\'')
            
            #check against each platform
            for platform, domains in PLATFORMS.items():
                for domain in domains:
                    if domain in clean_word.lower():
                        # Ensure we have the full URL
                        if not clean_word.startswith(('http://', 'https://')):
                            clean_word = 'https://' + clean_word
                        found_links[platform] = clean_word
                        break
                    
            # check for portfolio links
            if 'portfolio' not in found_links:
                if any(keyword in self.text.lower() for keyword in PORTFOLIO_KEYWORDS):
                    if ('.' in clean_word and 
                        not any(domain in clean_word.lower() for domain in ['.com', '.net', '.org']) and
                        len(clean_word.split('.')[-1]) >= 2):
                        found_links['portfolio'] = clean_word
        
        return found_links
    
# experinece
    # not working 
    def extract_experience_section0(self):
            section_patterns = [
                r"\bprofessional experience\b",
                r"\bwork experience\b",
                r"\bexperience\b",
                r"\bemployment history\b",
                r"\bcareer history\b",
                r"\brelevant experience\b",
                r"\bprofessional background\b"
            ]

            # combine into one regex with OR
            pattern = re.compile(r"(?i)(" + "|".join(section_patterns) + r")")

            #find all matches of section headers
            matches = list(pattern.finditer(self.text))










            if not matches:
                return ""

            #start from the first matched section
            start_index = matches[0].start()

            #define possible following section headers
            #next_section_pattern = re.compile(r"(?i)\b(education|skills|projects|certifications|languages|summary|profile|contact)\b")
            
            next_section_pattern = re.compile(
                    r"(?i)\b("
                    r"contact information|"
                    r"contact|"
                    r"objective|"
                    r"summary|"
                    r"professional summary|"
                    r"education|"
                    r"skills|"
                    r"projects|"
                    r"certifications|"
                    r"licenses|"
                    r"awards|"
                    r"honors|"
                    r"publications|"
                    r"references|"
                    r"technical skills|"
                    r"computer skills|"
                    r"computerskills|"
                    r"programming languages|"
                    r"software skills|"
                    r"soft skills|"
                    r"language skills|"
                    r"languages|"
                    r"professional skills|"
                    r"transferable skills|"
                    r"profile"
                    r")\b"
                )


            following_matches = list(next_section_pattern.finditer(self.text[start_index:]))

            if following_matches:
                end_index = start_index + following_matches[0].start()
            else:
                end_index = len(self.clean_text)

            experience_section = self.clean_text[start_index:end_index].strip()
            return experience_section


# experience 
  # working 

    def extract_experience_section1(self) -> list:
        """
        Extract the Experience section from the CV text.

        Returns:
            list: A list of experience entries, where each entry is a string or dictionary.
        """
        # Match the Experience section as a standalone section header
        pattern = re.compile(
            r"(?:\n|^)(Experience|Professional Experience|Work History|Employment History|Career History|Relevant Experience|Work Experience)\b\s*[:\-]?\s*\n(.*?)(?=\n{2,}|\n(?:Skills|Education|Projects|Certifications|[A-Z][a-zA-Z]*\s*[:\-])|\Z)",
            re.DOTALL | re.IGNORECASE
        )
        match = pattern.search(self.text)

        if match:
            experience_text = match.group(2).strip()
            print(f"Extracted experience text: {experience_text}")  # Debug print

            # Split the experience section into individual entries (based on dates or job titles)
            # Look for lines starting with dates (e.g., "2017-Present") or job titles
            entries = re.split(r"\n(?=\d{4}\s*(?:-|to|\–|\—)\s*(?:\d{4}|Present|Current))", experience_text, flags=re.IGNORECASE)

            experience_entries = []
            for entry in entries:
                entry = entry.strip()
                if not entry:
                    continue

                # Clean up the entry: replace newlines with spaces, handle bullet points
                entry = re.sub(r"\n\s*(?:[•\u2022]?\s*)?", ", ", entry)
                entry = re.sub(r"\s{2,}", " ", entry).strip()
                if entry:
                    experience_entries.append(entry)

            print(f"Parsed experience entries: {experience_entries}")  # Debug print
            return experience_entries

        print("No Experience section found.")  # Debug print
        return []




    #####################################################""
    #####################################################
    ################################################"
    # #########################################
    # 
    # ################""""""""""""""""""
    # "
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # sections  limiting 

    def _normalize_text(self, text: str) -> str:
        """
        Normalize the text to ensure consistent formatting for section detection.

        Args:
            text (str): The raw text to normalize.

        Returns:
            str: The normalized text.
        """
        # Replace multiple newlines with a single newline
        text = re.sub(r"\n\s*\n+", "\n", text)
        # Normalize spaces
        text = re.sub(r"\s+", " ", text)
        # Ensure section headers are on their own lines
        section_headers = [
            "Professional Summary", "Skills", "Core Competencies", "Technical Skills",
            "Key Skills", "Professional Skills", "Programming Skills", "Tech Stack",
            "Work Experience", "Professional Experience", "Work History","Employment History",
            "Career History", "Relevant Experience", "Experience", "Education",
            "Projects", "Certifications"
        ]
        for header in section_headers:
            text = re.sub(
                rf"(?<!\w){header}(?!\w)",
                f"\n{header}\n",
                text,
                flags=re.IGNORECASE
            )
        return text.strip()

    def _map_sections(self) -> dict:
        """
        Map all sections in the resume text to their start and end positions.

        Returns:
            dict: A dictionary mapping section names to their (start, end) positions.
        """
        normalized_text = self._normalize_text(self.text)
        lines = normalized_text.split("\n")
        sections = {}
        current_section = None
        start_pos = 0

        # Regex to identify section headers, including numbered sections like "1 EDUCATION"
        section_pattern = re.compile(
            r"^(Professional Summary|Skills|Core Competencies|Technical Skills|Key Skills|Professional Skills|Programming Skills|Tech Stack|Work Experience|Professional Experience|Work History|Employment History|Career History|Relevant Experience|Work Experience|Education|Projects|Certifications|[0-9\s]*(Education|Certifications))\b",
            re.IGNORECASE
        )

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Check if the line is a section header
            match = section_pattern.match(line)
            if match:
                # If we were already in a section, mark its end
                if current_section:
                    sections[current_section] = (start_pos, i)
                # Start a new section
                current_section = match.group(0).upper()
                start_pos = i + 1  # Start after the header

        # Mark the end of the last section
        if current_section:
            sections[current_section] = (start_pos, len(lines))

        print(f"Section map: {sections}")  # Debug print
        return sections

    def _extract_section_content(self, section_name: str) -> str:
        """
        Extract the content of a specific section using the section map.

        Args:
            section_name (str): The name of the section to extract (case-insensitive).

        Returns:
            str: The content of the section, or empty string if not found.
        """
        normalized_text = self._normalize_text(self.text)
        lines = normalized_text.split("\n")
        section_name_upper = section_name.upper()

        for section, (start, end) in self.sections.items():
            if section_name_upper in section:
                section_content = "\n".join(lines[start:end]).strip()
                print(f"Extracted content for {section_name}: {section_content}")  # Debug print
                return section_content

        print(f"Section {section_name} not found in section map.")  # Debug print
        return ""

    def extract_experience_section1111(self) -> list:
        """
        Extract the Experience section from the CV text.

        Returns:
            list: A list of experience entries, where each entry is a dictionary with job details.
        """
        experience_text = self._extract_section_content("Experience")
        if not experience_text:
            print("No Experience section found.")
            return []

        # Split the experience section into individual entries based on dates
        entries = re.split(
            r"\n(?=(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}\s*(?:-|to|\–|\—)\s*(?:\d{4}|Present|Current)|\d{4}\s*(?:-|to|\–|\—)\s*(?:\d{4}|Present|Current))",
            experience_text,
            flags=re.IGNORECASE
        )

        experience_entries = []
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            # Extract date range
            date_match = re.search(
                r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}\s*(?:-|to|\–|\—)\s*(?:\d{4}|Present|Current)|\d{4}\s*(?:-|to|\–|\—)\s*(?:\d{4}|Present|Current))",
                entry,
                re.IGNORECASE
            )
            if date_match:
                date = date_match.group(1)
                rest = entry[:date_match.start()].strip() + entry[date_match.end():].strip()
            else:
                date = ""
                rest = entry

            # Split the rest into job info and responsibilities
            lines = re.split(r"\n\s*(?:[•\u2022]?\s*)?", rest)
            job_info = lines[0].strip() if lines and lines[0].strip() else ""
            responsibilities = [line.strip() for line in lines[1:] if line.strip()]

            experience_entry = {
                "date": date,
                "job_info": job_info,
                "responsibilities": responsibilities
            }
            experience_entries.append(experience_entry)

        print(f"Parsed experience entries: {experience_entries}")  # Debug print
        return experience_entries


    def extract_skills_section111(self) -> list:
            """
            Extract the Skills section from the CV text.

            Returns:
                list: A list of skills extracted from the Skills section.
            """
            skills_text = self._extract_section_content("Skills")
            if not skills_text:
                print("No Skills section found.")
                return []

            # Split on newlines and bullet points to get individual skills
            raw_skills = re.split(r"\n\s*(?:[•\u2022]?\s*)?", skills_text)

            # Clean each skill: remove leading bullet points, trailing punctuation, and filter out short/empty entries
            skills = [
                re.sub(r"^[•\u2022]?\s*|[.,;]$", "", skill.strip())
                for skill in raw_skills
                if len(skill.strip()) > 1 and skill.strip()
            ]
            print(f"Parsed skills: {skills}")  # Debug print

            return skills


















# using AI to extract



# skills with ai
    def extract_skills_ai(self) -> list:
        """
        Uses an AI model to extract the Skills section from the text (resume).

        Returns:
            list: A list of skills extracted from the Skills section.
        """
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        prompt = skills_extractor_prompt.format(content=self.text)

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(content=self.text)
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

        try:
            parsed_result = json.loads(result.strip())
            return parsed_result.get("skills_section", [])
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in extract_skills_ai: {e}, Raw output: {result}")
            return []
        







# experience with ai
 
    def extract_experience_ai(self) -> list:
        """
        Uses an AI model to extract the Experience section from the text (resume).

        Returns:
            list: A list of experience entries, where each entry is a dictionary with job details.
        """
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        prompt = experience_extractor_prompt.format(content=self.text)

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(content=self.text)
                }
            ],
            temperature=0.3,
            max_completion_tokens=2048,
            top_p=1,
            stream=True,
            stop=None,
        )

        result = ""
        for chunk in completion:
            result += chunk.choices[0].delta.content or ""

        try:
            parsed_result = json.loads(result.strip())
            return parsed_result.get("experience_section", [])
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in extract_experience_ai: {e}, Raw output: {result}")
            return []














#education with ai

    def extract_education_ai(self) -> list:
        """
        Uses an AI model to extract the Education section from the text (resume).

        Returns:
            list: A list of education entries, where each entry is a dictionary with education details.
        """
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # Define the prompt to extract the Education section
        prompt = education_extractor_prompt.format(content=self.text)

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(content=self.text)
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

        # Parse the JSON string and return the education list
        try:
            parsed_result = json.loads(result.strip())
            return parsed_result.get("education_section", [])
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in extract_education_ai: {e}, Raw output: {result}")
            return []