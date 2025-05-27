experience_extractor_prompt = """
        You are an expert resume parser. Given the following resume text, extract the 'Work Experience' section (also known as 'Experience', 'Professional Experience', etc.). Format the output as a JSON-compatible string containing a single key "experience_section", whose value is a list of dictionaries. Each dictionary should contain:
        - "date": The date range of the job (e.g., "June 2018- Present").
        - "job_info": The job title, company, location, and any additional details on the same line (e.g., "Full Stack Java Developer, ABC Company, Inc., Anywhere, USA").
        - "responsibilities": A list of strings representing the job responsibilities (remove bullet points and preserve the text as full sentences).

        Resume text:
        {content}

        Return only the JSON-compatible string, with no additional text or explanations.
        """