import textacy  #used for text processing and analysis  built on spaCy
from textacy import extract # used for keyterm extraction
from collections import Counter

from textacy.extract.keyterms import sgrank
from spacy.tokens import Doc

#Each method in the cxlass extracts key terms using different algorithms.
class KeytermExtractor:
    """
    A class for extracting keyterms from a given text using various algorithms.
    """

    def __init__(self, raw_text: str, top_n_values: int = 20):
        """
        Initialize the KeytermExtractor object.

        Args:
            raw_text (str): The raw input text.
            top_n_values (int): The number of top keyterms to extract.
        """
        self.raw_text = raw_text # storing the raw input text
        self.text_doc = textacy.make_spacy_doc(self.raw_text, lang="en_core_web_md")

        # convert raw text into spacy document using a specified language medel 
        self.top_n_values = top_n_values # store the number of top keyterms to extract

    

    def get_combined_keyterms_old(self):
        """
        Combine keyterms from multiple extraction methods and rank them.

        Returns:
            List[str]: A ranked list of unique keyterms aggregated from all methods.
        """
        all_keywords = []

        # Get keywords from all available methods
        methods = [
            self.get_keyterms_based_on_textrank(),
            self.get_keyterms_based_on_sgrank(),
            self.get_keyterms_based_on_scake(),
            self.get_keyterms_based_on_yake(),
        ]

        for result in methods:
            # Each result is a list of tuples like: [('keyword1', 0.1), ...]
            for kw, _ in result:
                all_keywords.append(kw.lower())  # normalize to lowercase

        # Count occurrences (how many methods agreed on this keyword)
        keyword_freq = Counter(all_keywords)

        # Return most common ones, limited by top_n_values
        top_keywords = [kw for kw, _ in keyword_freq.most_common(self.top_n_values)]

        print(top_keywords)
        return top_keywords
    




    #05/05/2025


    def get_keyterms_based_on_sgrank_newest(self):
        """
        Extract keyterms using the SGRank algorithm, after filtering out names, organizations, and places.

        Returns:
            List[Tuple[str, float]]: A list of top keyterms and their scores based on SGRank.
        """
        excluded_ents = {"PERSON", "ORG", "GPE"}
        excluded_token_ids = set()

        # Identify token indices to exclude based on named entities
        for ent in self.text_doc.ents:
            if ent.label_ in excluded_ents:
                excluded_token_ids.update(range(ent.start, ent.end))

        # Build filtered text from tokens not in excluded named entities
        filtered_tokens = [token.text for token in self.text_doc if token.i not in excluded_token_ids]
        filtered_text = " ".join(filtered_tokens)

        # Recreate spaCy doc for SGRank
        filtered_doc = textacy.make_spacy_doc(filtered_text, lang="en_core_web_md")  # or 'en_core_web_trf'

        # Extract keyterms with scores
        keyterms = sgrank(filtered_doc, normalize="lemma", topn=self.top_n_values)

        return keyterms  # Returns list of tuples: (term, score)



    
















    def get_keyterms_based_on_textrank(self):
        """
        Extract keyterms using the TextRank algorithm.

        Returns:
            List[str]: A list of top keyterms based on TextRank.
        """
        return list(
            extract.keyterms.textrank(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )
    # TextRank: A graph-based ranking algorithm (similar to PageRank) 
    #that identifies key terms by analyzing word relationships.

    def get_keyterms_based_on_sgrank(self):
        """
        Extract keyterms using the SGRank algorithm.

        Returns:
            List[str]: A list of top keyterms based on SGRank.
        """
        return list(
            extract.keyterms.sgrank(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        ) 
    #SGRank: A supervised keyphrase extraction algorithm combining statistical and graph-based features.

    def get_keyterms_based_on_scake(self):
        """
        Extract keyterms using the sCAKE algorithm.

        Returns:
            List[str]: A list of top keyterms based on sCAKE.
        """
        return list(
            extract.keyterms.scake(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )
    #sCAKE: A scalable keyphrase extraction model that incorporates both co-occurrence and context.

    def get_keyterms_based_on_yake(self):
        """
        Extract keyterms using the YAKE algorithm.

        Returns:
            List[str]: A list of top keyterms based on YAKE.
        """
        return list(
            extract.keyterms.yake(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )
    # YAKE (Yet Another Keyword Extractor): A statistical method for extracting keywords based on word 
    # frequency, position, and other linguistic properties.
    

    #N-Gram Chunking Methods

    #These methods generate 
    # bigrams (2-word sequences) 
    #  trigrams (3-word sequences).
    def bi_gramchunker(self):
        """
        Chunk the text into bigrams.

        Returns:
            List[str]: A list of bigrams.
        """
        return list(
            textacy.extract.basics.ngrams(
                self.text_doc,
                n=2,
                filter_stops=True,
                filter_nums=True,
                filter_punct=True,
            )
        )

    def tri_gramchunker(self):
        """
        Chunk the text into trigrams.

        Returns:
            List[str]: A list of trigrams.
        """
        return list(
            textacy.extract.basics.ngrams(
                self.text_doc,
                n=3,
                filter_stops=True,
                filter_nums=True,
                filter_punct=True,
            )
        )
