import re
from uuid import uuid4

import spacy
import string # used to acess common punctuation symbols

import nltk # import the NLTK (Natural Language Toolkit liberay) 
from nltk.corpus import stopwords #import NLTK's stopwords corpus
from nltk.stem import WordNetLemmatizer #import NLTK's WordNet lemmatizer
from nltk.tokenize import word_tokenize #import  NLTK's word tokenizer

# Load the English model
nlp = spacy.load("en_core_web_md")

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
}


def generate_unique_id():
    """
    Generate a unique ID and return it as a string.

    Returns:
        str: A string with a unique ID.
    """
    return str(uuid4())

'''
class TextCleaner:
    """
    A class for cleaning a text by removing specific patterns.
    """

    def remove_emails_links(text):
        """
        Clean the input text by removing specific patterns.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], "", text)
        return text

    def clean_text(text):
        """
        Clean the input text by removing specific patterns.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        text = TextCleaner.remove_emails_links(text)
        doc = nlp(text)
        for token in doc:
            if token.pos_ == "PUNCT":
                text = text.replace(token.text, "")
        return str(text)

    def remove_stopwords(text):
        """
        Clean the input text by removing stopwords.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        doc = nlp(text)
        for token in doc:
            if token.is_stop:
                text = text.replace(token.text, "")
        return text
    
    '''
class TextCleaner:

    def __init__(self, raw_text):
        #initialization for the stopwords_set with english stopwords and punctuation
        self.stopwords_set = set(stopwords.words("english") + list(string.punctuation))
        
        """
            what's a Lemmatize?
            Lemmatization is the process of grouping together the different inflected forms of a word so they
            can be analyzed as a single item. For example, running, runs, ran, and run
            
            it is very important in NLP because it helps normallize words so that different forms of the same word are treated as identical,
            symplifying the analysis and interpretation of text.

            In the NLTK library (Natural Language Toolkit) in Python, the WordNetLemmatizer class is commonly used for lemmatization.
            It uses WordNet, a lexical database of English, to map words to their lemmas based on their part of speech.
        """

        self.lemmatizer = WordNetLemmatizer() # Initializes WordNetLemmatizer, which reduces words to their base form (lemma)
        # Stores the original text in an instance variable.
        self.raw_input_text = raw_text

    def clean_text(self) -> str:
        text = re.sub(r"[^\w\s]", "", self.raw_input_text)  # Remove special characters (e.g., ♂, ¶)
        text = re.sub(r'\b\w*\d\w*\b', '', text)  # Remove words with digits (e.g., "Engineer321")



        tokens = word_tokenize(text.lower())#Tokenize and convert text to lowercase
        

        #tokens = word_tokenize(self.raw_input_text.lower()) 



        tokens = [token for token in tokens if token not in self.stopwords_set] #removes stopwords and puntuation from tokens
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens] #lemmatize tokens to their base form
        cleaned_text = " ".join(tokens) # Join tokens back into a cleaned text string
        return cleaned_text



class CountFrequency:

    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)

    def count_frequency(self):
        """
        Count the frequency of words in the input text.

        Returns:
            dict: A dictionary with the words as keys and the frequency as values.
        """
        pos_freq = {}
        for token in self.doc:
            if token.pos_ in pos_freq:
                pos_freq[token.pos_] += 1
            else:
                pos_freq[token.pos_] = 1
        return pos_freq
