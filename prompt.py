PROMPT_TEMPLATE = """Analyze the match between this resume and job description.
Return ONLY a numerical percentage (0-100) with no additional text or symbols.

Resume:
{resume}

Job Description:
{job_description}

Match Percentage:"""




# we don't use f"""   """
# Python will try to substitute resume immediately 
# but resume is not defined inside prompt.py.
# This will throw a NameError: name 'resume' is not defined'

ats_prompt = """
Hey, act like a highly experienced and skilled Applicant Tracking System (ATS) with deep knowledge of the tech and IT fields, including software engineering, data science, data analysis, and big data engineering roles.

Your task is to analyze how well this resume matches the given job description. The job market is extremely competitive, so be precise and thorough. Use your expertise in evaluating both technical and soft skills, tool proficiency, experience, and keyword relevance.

Return ONLY a numerical percentage (0-100) with no additional text or symbols.


Resume content:
{resume}

Job Description:
{job_description}
"""




"""
Return a JSON object with the following:
- "match_percentage": (number from 0 to 100, based on how well the resume matches the job description)
- "missing_keywords": (a list of important keywords from the job description that are missing in the resume)
- "recommendations": (concise tips to improve the resume for better alignment with the job description)

"""