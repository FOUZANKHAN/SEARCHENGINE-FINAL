from .querycomponent import QueryComponent
from indexing import Index, Posting
import merger_postings
from functools import reduce
from queries import querycomponent
from text import ProjectTokenProcessor

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components
# TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
# merging the resulting postings.
    def get_postings(self, index : Index, token_processor: ProjectTokenProcessor) -> list[Posting]:
        result = []
        componentPostings = []
        # get postings for all the components
        for component in self.components:
            posting = component.get_postings(index, token_processor)
            componentPostings.append(posting)

        merged_list = reduce(merger_postings.or_merge, componentPostings)
        #print(merged_list)
        result = merged_list
        return result

    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"
