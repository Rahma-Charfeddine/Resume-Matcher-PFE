skills_extractor_prompt = """
You are an expert resume parser. Given the following resume text, extract the 'Skills' section.
Format the output as a JSON-compatible string containing a single key "skills_section", whose value is a list of strings. Each string should be a skill, with bullet points removed and the text cleaned up (e.g., remove trailing punctuation, normalize spaces).

        Resume text:
        {content}

        Return only the JSON-compatible string, with no additional text or explanations.
        """