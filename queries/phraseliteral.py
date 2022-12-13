from indexing.postings import Posting
from .querycomponent import QueryComponent
from . import TermLiteral
import merger_postings
from text import ProjectTokenProcessor
from indexing import DiskPositionalIndex

class PhraseLiteral(QueryComponent):
    """Represents a phrase literal consisting of one or more terms that must occur in sequence."""
    def __init__(self, terms : list[str], is_not: bool):
        self.terms = terms.split(" ")
        self.is_not = is_not
# TODO: program this method. Retrieve the postings for the individual terms in the phrase,
# and positional merge them together.
    def get_postings(self, index,token_processor:ProjectTokenProcessor) -> list[Posting]:
        result = [Posting]
        componentPostings = [] #posting components
        for term in self.terms: #processing each term in self.terms
            term_literal = TermLiteral(term, False) #creating a term literal object and finding the postinsg related to it
            # if index!=DiskPositionalIndex:
            #     posting = term_literal.get_postings(index,token_processor)
            # else:
            posting = term_literal.get_positional_postings(index,token_processor)#change this to make the phrase and near work for milestopne 1
            componentPostings.append(posting)

        posting1 = componentPostings[0]

        if len(componentPostings) == 1:
            return posting1

        else: #I liked the way to get an offset
            for i in range(1,len(componentPostings)):
                postingnxt = componentPostings[i]
                posting1 = merger_postings.merge_phrase(posting1, postingnxt, i)
                #created an merger posting file that and merger, or merger and phrase merge

            result = posting1
            return posting1


    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
