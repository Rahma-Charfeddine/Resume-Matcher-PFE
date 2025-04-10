import textacy  #used for text processing and analysis  built on spaCy
from textacy import extract # used for keyterm extraction

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
