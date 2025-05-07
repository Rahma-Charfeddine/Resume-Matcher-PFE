
from scripts.parsers.ParseResumeToJson import ParseResume

# Sample resume text to test
resume= """

John Doe

Phone: +1 (555) 123-4567

LinkedIn: linkedin.com/in/johndoe



New York, usa



Professional Summary:
Experienced software engineer with a strong background in Python, machine learning, and cloud technologies.

Skills:
Python, Java, AWS, Docker, Kubernetes, SQL, Machine Learning, Data Analysis

Experience:
Software Engineer at TechCorp (2019 - 2023)
- Built scalable backend systems using Python and Django.
- Deployed machine learning models to AWS using Docker.

Education:
Bachelor of Science in Computer Science - University of Technology, 2015 - 2019


- Email: john.doe@example.com
- LinkedIn: linkedin.com/in/johndoe
- GitHub: github.com/johndoe
- GitLab: gitlab.com/johndoe

LinkedIn: linkedin.com/in/johndoe 
GitHub: www.github.com/johndoe
Portfolio: janesmith.dev
Contact me at 
Invalid: a@b.c, @example.com, user@.com


"""

# Parse the resume
#parsed_resume = ParseResume(resume_text)
output = ParseResume(resume).get_JSON()


# Get the JSON output
#parsed_data = parsed_resume.get_JSON()

# Print parsed data (optional: filter specific sections)
#from pprint import pprint
#pprint(parsed_data)
print(output)