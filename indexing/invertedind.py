from typing import Iterable
from . import Posting, Index

class InvertedInd(Index):

    def __init__(self, corpus_size : int):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self.corpus_size = corpus_size
        self.dictionary = {}

    def add_term(self, term : str, doc_id : int):
        """Records that the given term occurred in the given document ID."""
        if term in self.dictionary.keys():
            if self.dictionary[term][-1] != doc_id:
                self.dictionary[term].append(doc_id)
        else:
            self.dictionary[term] = [doc_id]
        #self.dictionary[term] = sorted(self.dictionary[term])

    #def get_vocabulary(self, term : str) -> Iterable[str]:
            #self.dictionary[term] = sorted(self.dictionary[term])


    def get_postings(self,term : str)-> Iterable[Posting]:
        try:
            docs_that_have_them = []
            if term in self.dictionary.keys():
                for ids in self.dictionary[term]:
                    docs_that_have_them.append(Posting(ids))
                return (docs_that_have_them)
        except TypeError:
            print("There is no such word in the corpus")

    def __str__(self) -> str:
        return str(self.dictionary)
