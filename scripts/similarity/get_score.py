

# importing libraries
import json
import logging
import os
import numpy as np
from typing import List
import requests
import yaml
import re
#for gemini
#import google.generativeai as genai

#from prompt import PROMPT_TEMPLATE
#from prompt import ats_prompt
from prompt_templates.ats_score_prompt import ats_prompt




### pip install sentence-transformers qdrant-client scikit-learn


#from typing import List
#from sentence_transformers import SentenceTransformer

#for model deepseek
#import torch
#from transformers import AutoTokenizer, AutoModel

#from sklearn.metrics.pairwise import cosine_similarity
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams

from scripts.utils.logger import init_logging_config



# Logging is a mechanism to track events that occur when software runs.
#  It is especially useful for debugging, monitoring, and diagnosing
#  issues in the  application.



# initialize the logging configuration
init_logging_config(basic_log_level=logging.INFO)
# Get the logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)


#  Load pre-trainedsentence embedding model and Qdrant client 

# all-mpnet-base-v2
#model = SentenceTransformer('all-mpnet-base-v2')

# all-MiniLM-L6-v2
#model = SentenceTransformer('all-MiniLM-L6-v2')


# BAAI/bge-large-en
#model = SentenceTransformer('BAAI/bge-large-en')


#print("Embedding Size:", model.get_sentence_embedding_dimension())  



#for deepseek
'''
model_name = "deepseek-ai/DeepSeek-R1"
#tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1")
#model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-R1")

tokenizer = AutoTokenizer.from_pretrained(model_name ,  trust_remote_code=True)
model = AutoModel.from_pretrained(model_name,  trust_remote_code=True)

'''
# Qdrant is an open-source vector search engine designed for fast and scalable similarity search
# Use persistent Qdrant instance
#client = QdrantClient("http://localhost:6333")  
client = QdrantClient(":memory:")
# Define collection
collection_name = "resume_matching"
#for model 1
#vector_params = VectorParams(size=384, distance="Cosine")

# for all-mpnet-base-v2
#vector_params = VectorParams(size=768, distance="Cosine")

#for model deep seek # needs authentication 
#vector_params = VectorParams(size=384, distance="Cosine")

# for all-MiniLM-L6-v2
#vector_params = VectorParams(size=384, distance="Cosine")

# for BAAI/bge-large-en # takes to much time 
#vector_params = VectorParams(size=1024, distance="Cosine")




'''
# Ensure collection exists
if not client.collection_exists(collection_name):
    client.create_collection(collection_name=collection_name, vectors_config=vector_params)
'''


# function find_path

def find_path(folder_name):
    """
    The function `find_path` searches for a folder by name starting from the current directory and
    traversing up the directory tree until the folder is found or the root directory is reached.

    Args:
      folder_name: The `find_path` function you provided is designed to search for a folder by name
    starting from the current working directory and moving up the directory tree until it finds the
    folder or reaches the root directory.

    Returns:
      The `find_path` function is designed to search for a folder with the given `folder_name` starting
    from the current working directory (`os.getcwd()`). It iterates through the directory structure,
    checking if the folder exists in the current directory or any of its parent directories. If the
    folder is found, it returns the full path to that folder using `os.path.join(curr_dir, folder_name)`
    """
    curr_dir = os.getcwd()
    while True:
        if folder_name in os.listdir(curr_dir):
            return os.path.join(curr_dir, folder_name)
        else:
            parent_dir = os.path.dirname(curr_dir)
            if parent_dir == "/":
                break
            curr_dir = parent_dir
    raise ValueError(f"Folder '{folder_name}' not found.")


cwd = find_path("Resume-Matcher")
READ_RESUME_FROM = os.path.join(cwd, "Data", "Processed", "Resumes")
READ_JOB_DESCRIPTION_FROM = os.path.join(cwd, "Data", "Processed", "JobDescription")
config_path = os.path.join(cwd, "scripts", "similarity")



#function read_config
def read_config(filepath):
    """
    The `read_config` function reads a configuration file in YAML format and handles exceptions related
    to file not found or parsing errors.

    Args:
      filepath: The `filepath` parameter in the `read_config` function is a string that represents the
    path to the configuration file that you want to read and parse. This function attempts to open the
    file specified by `filepath`, load its contents as YAML, and return the parsed configuration. If any
    errors occur during

    Returns:
      The function `read_config` will return the configuration loaded from the file if successful, or
    `None` if there was an error during the process.
    """
    try:
        with open(filepath) as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError as e:
        logger.error(f"Configuration file {filepath} not found: {e}")
    except yaml.YAMLError as e:
        logger.error(
            f"Error parsing YAML in configuration file {filepath}: {e}", exc_info=True
        )
    except Exception as e:
        logger.error(f"Error reading configuration file {filepath}: {e}")
    return None


def read_doc(path):
    """
    The `read_doc` function reads a JSON file from the specified path and returns its contents, handling
    any exceptions that may occur during the process.

    Args:
      path: The `path` parameter in the `read_doc` function is a string that represents the file path to
    the JSON document that you want to read and load. This function reads the JSON data from the file
    located at the specified path.

    Returns:
      The function `read_doc(path)` reads a JSON file located at the specified `path`, and returns the
    data loaded from the file. If there is an error reading the JSON file, it logs the error message and
    returns an empty dictionary `{}`.
    """
    with open(path) as f:
        try:
            data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            data = {}
    return data


#def get_score(resume_string, job_description_string):
    """
    The function `get_score` uses QdrantClient to calculate the similarity score between a resume and a
    job description.

    Args:
      resume_string: The `resume_string` parameter is a string containing the text of a resume. It
    represents the content of a resume that you want to compare with a job description.
      job_description_string: The `get_score` function you provided seems to be using a QdrantClient to
    calculate the similarity score between a resume and a job description. The function takes in two
    parameters: `resume_string` and `job_description_string`, where `resume_string` is the text content
    of the resume and

    Returns:
      The function `get_score` returns the search result obtained by querying a QdrantClient with the
    job description string against the resume string provided.
    """

    # first version
    '''
    logger.info("Started getting similarity score")

    documents: List[str] = [resume_string]
    client = QdrantClient(":memory:")
    #client.set_model("BAAI/bge-base-en")
    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    client.add(
        collection_name="demo_collection",
        documents=documents,
    )

    search_result = client.query(
        collection_name="demo_collection", query_text=job_description_string
    )
    logger.info("Finished getting similarity score")
    return search_result

    '''
    ### newest version #######

    '''
    # Generate embeddings
    logger.info("Started getting similarity score")
    resume_embedding = model.encode([resume_string])[0]  
    job_desc_embedding = model.encode([job_description_string])[0]

    # Insert resume embedding into Qdrant (use a unique ID for each resume)
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=1, vector=resume_embedding.tolist())]
    )

    # Query for similarity
    search_result = client.search(
        collection_name=collection_name,
        query_vector=job_desc_embedding.tolist(),
        limit=1
    )
    logger.info("Finished getting similarity score")
    # Return only the similarity score (or 0 if no match found)
    return search_result
    '''
    
# trial  2 : model 2
# latest version 08/04/2025
'''
def get_score(resume_string, job_description_string):
    logger.info("Started getting similarity score")

    resume_embedding = model.encode([resume_string])[0]
    job_desc_embedding = model.encode([job_description_string])[0]

    if resume_embedding is None or len(resume_embedding) == 0:

        raise ValueError("Resume embedding is empty!")

    if job_desc_embedding is None or len(job_desc_embedding) == 0:
        raise ValueError("Job description embedding is empty!")

    print("Resume Embedding Shape:", resume_embedding.shape)
    print("Job Description Embedding Shape:", job_desc_embedding.shape)
  
    # Normalize vectors
    resume_embedding = resume_embedding / np.linalg.norm(resume_embedding)
    job_desc_embedding = job_desc_embedding / np.linalg.norm(job_desc_embedding)

    # Ensure collection exists
    if not client.collection_exists(collection_name):
        client.create_collection(collection_name=collection_name, vectors_config=vector_params)

    # Insert resume embedding
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=1, vector=resume_embedding.tolist())]
    )

    # Query for similarity
    search_result = client.search(
        collection_name=collection_name,
        query_vector=job_desc_embedding.tolist(),
        limit=1
    )

    logger.info("Finished getting similarity score")

    # Return only the similarity score (or 0 if no match found)
    return search_result[0].score if search_result else 0
'''
'''
#using LLM
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)



def get_score(resume_string, job_description_string):
    logger.info("Started getting similarity score using Hugging Face Inference API")

    # Prepare the prompt for the model
    prompt = f"""
    You are a job matching assistant. Please provide a score between 0 and 100 based on the relevance of the resume to the job description.
    
    Resume: {resume_string}

    Job Description: {job_description_string}

    Score:
    """
    
    # Set up the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}"  # Use your Hugging Face API key for authorization
    }
    
    # Call the Hugging Face Inference API
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistral/mistral-7b-instruct-v0.1",
        headers=headers,
        json={"inputs": prompt}
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        score = response.json()[0]["generated_text"]
        score_value = score.split("Score:")[-1].strip()  # Extract the score value
        logger.info("Finished getting similarity score")
        return score_value
    else:
        logger.error(f"Error: {response.status_code}, Message: {response.text}")
        return None
'''

# TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
#TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf
# downloaded locally
#version 1
'''
def get_score(resume, job_description):
    prompt = f"""
    You are an expert recruiter...

    Job: {job_description}
    Resume: {resume}

    Rate the match out of 100 and explain.
    """

    response = requests.post(
        "http://127.0.0.1:5000/v1/completions",
        json={"prompt": prompt, "max_tokens": 300}
    )

    return response.json()['text']
'''
# TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
#TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf
#version 2

'''
def get_score(resume, job_description):
    prompt = f"""Analyze this resume-job match:
    Resume: {resume}
    Job: {job_description}
    Return ONLY a percentage (0-100) """
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/generate",
            json={
                "prompt": prompt,
                "max_new_tokens": 150,
                "temperature": 0.1  # More deterministic
            },
            timeout=120
        )
        response.raise_for_status()
        
        # Handle different response formats
        data = response.json()
        
        if 'results' in data:
            result_text = data['results'][0]['text']
        elif 'choices' in data:
            result_text = data['choices'][0]['text']
        else:
            logger.warning("Unexpected response format, returning default value.")
            return "50"  # Default if parsing fails

        # Extract percentage from the result text
        try:
            # Assuming the response text format is "X% - explanation"
            percentage = float(result_text.split('%')[0].strip())
            return percentage
        except (ValueError, IndexError) as e:
            logger.error(f"Error extracting percentage: {e}")
            return "50"  # Fallback value

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        return "50"  # Fallback value
'''


# TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
#TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf
#version 3

'''
def get_score(resume, job_description):
    prompt = f"""Analyze this resume-job match:
    Resume: {resume}
    Job: {job_description}
    Return ONLY a percentage (0-100) """
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/v1/completions",
            json={
                "prompt": prompt,
                "max_new_tokens": 150,
                "temperature": 0.1  
            },
            timeout=180
        )
        response.raise_for_status()
        
        # Handle different response formats
        data = response.json()
        
        if 'results' in data:
            result_text = data['results'][0]['text']
        elif 'choices' in data:
            result_text = data['choices'][0]['text']
        else:
            logger.warning("Unexpected response format, returning default value.")
            return "50"  # Default if parsing fails

        # Extract percentage from the result text
        try:
            # Assuming the response text format is "X% - explanation"
            percentage = float(result_text.split('%')[0].strip())
            return percentage
        except (ValueError, IndexError) as e:
            logger.error(f"Error extracting percentage: {e}")
            return "50"  # Fallback value

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        return "50"  # Fallback value
'''


'''
def get_score(resume_string, job_description_string):
    logger.info("Started getting similarity score")
    
    # Tokenize and generate embeddings
    resume_inputs = tokenizer(resume_string, return_tensors="pt", padding=True, truncation=True)
    job_desc_inputs = tokenizer(job_description_string, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        resume_embedding = model(**resume_inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
        job_desc_embedding = model(**job_desc_inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
    
    # Insert resume embedding into Qdrant
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=1, vector=resume_embedding.tolist())]
    )
    
    # Query for similarity
    search_result = client.search(
        collection_name=collection_name,
        query_vector=job_desc_embedding.tolist(),
        limit=1
    )
    
    logger.info("Finished getting similarity score")
    return search_result
'''









# gemini API
# not for free
'''
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Store key in .env file
model = genai.GenerativeModel(model_name='gemini-pro')



def get_score(resume, job_description):
    prompt = f"""Analyze the match between this resume and job description.
    Return ONLY a numerical percentage (0-100) with no additional text or symbols.
    
    Resume:
    {resume}
    
    Job Description:
    {job_description}
    
    Match Percentage: """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 10,  # We only need a number
                "temperature": 0.1,       # Low for deterministic results
                "top_p": 0.95
            }
        )
        
        # Extract the percentage (Gemini returns Markdown formatted text)
        result_text = response.text.strip()
        
        # Handle cases where Gemini adds explanations
        if "%" in result_text:
            percentage = float(result_text.split("%")[0].strip())
        else:
            # Try to find first number in response
            percentage = float(''.join(filter(str.isdigit, result_text)))
            
        return min(max(percentage, 0), 100)  # Clamp to 0-100 range
        
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        return 50.0  # Fallback as float

    '''



# gemini for free
# gemini-1.5-flash'
# 17/04/2025
'''
genai.configure(api_key=os.getenv("Gemini_API_Key"))  # Store key in .env file
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def get_score(resume, job_description):
    prompt = PROMPT_TEMPLATE.format(resume=resume, job_description=job_description)

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()

        match = re.search(r'\d{1,3}', result)
        if match:
            score = int(match.group())
            return score if 0 <= score <= 100 else None
        else:
            return None
    except Exception as e:
        print("Error generating similarity score:", e)
        return None
'''



    





# wait for the access  to be accepted 
# meta-llama/Meta-Llama-3-8B-Instruct
'''
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv() 
hf_token = os.getenv("HF_API_KEY")

from huggingface_hub import InferenceClient

def get_score(resume, job_description):
    client = InferenceClient(token=hf_token)
    response = client.text_generation(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        prompt=f"""Analyze the match between this resume and job description.
        Return ONLY a numerical percentage (0-100) with no additional text or symbols.
        
        Resume:
        {resume}
        
        Job Description:
        {job_description}
        
        Match Percentage: """,
        max_new_tokens=50
    )
    return response.strip()
'''




# mixedbread-ai/mxbai-rerank-xsmall-v1
# a ranker LLM model
'''
def get_score(resume, job_description):
    client = InferenceClient(token=hf_token)
    response = client.text_generation(
        model="google/flan-t5-base",
        prompt=f"""Analyze the match between this resume and job description.
        Return ONLY a numerical percentage (0-100) with no additional text or symbols.
        
        Resume:
        {resume}
        
        Job Description:
        {job_description}
        
        Match Percentage: """,
        max_new_tokens=50
    )
    return response.strip()
'''


# Gemnini for free 

'''
import google.generativeai as genai
import os

genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel(model_name='gemini-1.5-flash')
response = model.generate_content('Teach me about how an LLM works')

print(response.text)
'''

# groq api  to import 
from groq import Groq

#client = Groq()


def get_score(resume, job_description):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    formatted_prompt = ats_prompt.format(
        resume=resume,
        job_description=job_description
    )
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                #"content": "Analyze the match between this resume and job description, Return ONLY a numerical percentage (0-100) i need a relevant result. \nthis is the keywords of the resume : " + resume +" \n and these are the keywords of the job description" + job_description
                "content": formatted_prompt
            }
            
        ],
    
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    
    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result.strip()



    
'''

if __name__ == "__main__":
    # To give your custom resume use this code
   
    resume_dict = read_config(
        READ_RESUME_FROM
        + "/Resume-alfred_pennyworth_pm.pdf83632b66-5cce-4322-a3c6-895ff7e3dd96.json"
    )
    job_dict = read_config(
        READ_JOB_DESCRIPTION_FROM
        + "/JobDescription-job_desc_product_manager.pdf6763dc68-12ff-4b32-b652-ccee195de071.json"
    )
    
    resume_dict = read_config(
        READ_RESUME_FROM
        + "/Resume-john_doe (1).pdf16c04dad-5b6b-4d5d-b645-f1a88fea3951.json"
    )
    job_dict = read_config(
        READ_JOB_DESCRIPTION_FROM
        + "/JobDescription-job_desc_front_end_engineer.pdf3016a680-fdba-40ff-80dc-9625ccff4150.json"
    )
    
    resume_keywords = resume_dict["extracted_keywords"]
    job_description_keywords = job_dict["extracted_keywords"]

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    final_result = get_score(resume_string, jd_string)
    for r in final_result:
        print(r.score)'
'''