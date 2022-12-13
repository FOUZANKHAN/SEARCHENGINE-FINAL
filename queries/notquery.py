from .querycomponent import QueryComponent
from indexing import Index, Posting
import merger_postings
from text import ProjectTokenProcessor
from . import TermLiteral
from queries import querycomponent

class NotQuery(QueryComponent):
    '''This was supposed to work for not query'''
    def __init__(self, component:QueryComponent, is_not: bool):
        self.component = component
        self.is_not = True

    def get_postings(self, index: Index, token_processor: ProjectTokenProcessor):
        result = [Posting]
        # term_lit = TermLiteral(self.component,self.is_not)
        #for i in range(0,len(self.component)):
        result = self.component.get_postings(index, token_processor)

        return result


    def __str__(self):
        return " NOT ".join(self.component)
