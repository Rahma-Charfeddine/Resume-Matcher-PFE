


parse_keywords_prompt = """
Act as an expert in resume parsing and job description analysis with deep understanding of IT, data science, software engineering, and big data roles.

Your task is to extract and return only the most relevant keywords from the following input.

The Keywords must not be or contain the words "linkedin", "github", "gitlab", "portfolio", "http", "https", "www"
 a Keyword  can not be a PERSON , organisation, Location, place , city or country 

 and each keyword must not be repeated

 also if your are extracting from a job description , ignore the parts talking about the company , the benefits or what they offer 

return only a list of the all relevant keywords (words not expressions )  of the input with no additional text or symbols only and don't say: Here is the list of relevant keywords: or any thing else, I need to see only the keywords not any other word or text 

Do not start your response with anything like this following Here is the list of relevant keywords: or anything similar , just the keywords only 
{content}
"""














"""
Separate them based on the type: technical skills, soft skills, tools, certifications, and general topics. Do NOT include explanations or extra text.

Format your response as a JSON object with the following keys:
- "technical_skills": []
- "soft_skills": []
- "tools": []
- "certifications": []
- "topics": []
"""