education_extractor_prompt = """
        You are an expert resume parser. Given the following resume text, extract the 'Education' section (also known as 'Academic Background', 'Educational Qualifications', etc.). Format the output as a JSON-compatible string containing a single key "education_section", whose value is a list of dictionaries. Each dictionary should contain:
        - "degree": The degree earned (e.g., "Bachelor of Science in Computer Science").
        - "institution": The name of the educational institution (e.g., "State University").
        - "location": The location of the institution (e.g., "Anywhere, USA").
        - "date": The graduation date or date range (e.g., "May 2016").

        If multiple education entries are present, include all of them in the list. If no Education section is found, return an empty list for "education_section".

        Resume text:
        {content}

        Return only the JSON-compatible string, with no additional text or explanations.
        """