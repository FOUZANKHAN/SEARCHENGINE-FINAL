from indexing.postings import Posting
from .querycomponent import QueryComponent
from text import ProjectTokenProcessor
from indexing import DiskPositionalIndex

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    # def __init__(self,term : str,is_not: bool ):
    #     self.term = term

    def __init__(self,term : str, is_not: bool ):
        self.term = term
        self.is_not = is_not

    def get_postings(self, index, token_processor: ProjectTokenProcessor) -> list[Posting]:
        tokenizedterm = token_processor.process_token(ProjectTokenProcessor, self.term)
        #print(f"this is in termliteral {tokenizedterm}")
        if tokenizedterm != "" or tokenizedterm != "-":
            posting = index.get_postings(tokenizedterm[0])
            if posting is not None:
                return posting
        # while("" in tokenizedterm):
        #     tokenizedterm.remove("")
        #     if [] in tokenizedterm:
        #         tokenizedterm.remove([])
        # if [] not in tokenizedterm:
        #     print(f"this is in termliteral {tokenizedterm}")
        
        
        
   
    # def get_wdt(self, index, token_processor: ProjectTokenProcessor) -> list[Posting]:
    #     tokenizedterm = token_processor.process_token(ProjectTokenProcessor, self.term)
    #     return index.get_postings(tokenizedterm[0])

    # new_list = []
        # for ele in tokenizedterm:
        #     if ele:
        #         new_list.append(ele)
        # print(f"this is in termliteral {new_list}")
    
    def get_positional_postings(self, index, token_processor: ProjectTokenProcessor) -> list[Posting]:
        tokenizedterm = token_processor.process_token(ProjectTokenProcessor, self.term)
        # if index != DiskPositionalIndex:
        #     return index.get_postings(tokenizedterm[0])
        return index.get_positional_postings(tokenizedterm[0])
         

    def __str__(self) -> str:
        return self.term
