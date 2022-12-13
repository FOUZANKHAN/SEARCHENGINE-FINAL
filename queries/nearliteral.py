from indexing.postings import Posting
from .querycomponent import QueryComponent
from . import TermLiteral
from text import ProjectTokenProcessor
import merger_postings

class NearLiteral(QueryComponent):

    def __init__(self, terms : list[str], is_not: bool):
        self.terms = terms.split(" ")
        self.first = self.terms[0] #firs numb
        self.k = self.terms[1].split('/')
        self.second = self.terms[2] #second numb
        self.is_not = is_not

    def get_postings(self, index, token_processor:ProjectTokenProcessor) -> list[Posting]:
        result = [Posting]
        first_toke_postings = TermLiteral(self.first, False).get_postings(index,token_processor)
        second_toke_postings = TermLiteral(self.second, False).get_postings(index, token_processor)

        postings = merger_postings.merge_phrase(first_toke_postings,second_toke_postings,int(self.k[1])+1)

        result = postings
        return result




    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
