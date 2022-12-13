from typing import Iterable
from . import Posting, Index
from text import ProjectTokenProcessor

class PositionalInvIndex(Index):

    def __init__(self, corpus_size : int):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self.corpus_size = corpus_size
        self.dictionary : dict[str, list[Posting]] = {}

    def add_term(self, term : str, doc_id : int, pos: int):
        """Records that the given term occurred in the given document ID."""
        if term in self.dictionary.keys():
            if self.dictionary[term][-1].doc_id != doc_id:
                self.dictionary[term].append(Posting(doc_id, [pos]))
            else:
                self.dictionary[term][-1].position_list.append(pos)
        else:
            self.dictionary[term] = [Posting(doc_id, [pos])]


    def vocabulary(self) -> str:
        vocab = []
        for term in self.dictionary.keys():
            vocab.append(term)
        vocab = sorted(vocab)
        return vocab


    def get_postings(self,term : str)-> Iterable[Posting]:
        try:
           return self.dictionary[term] if term in self.dictionary.keys() else []
        except TypeError:
            print("There is no such word in the corpus")


    def __str__(self) -> str:
        return str(self.dictionary)
