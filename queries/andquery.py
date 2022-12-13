from .querycomponent import QueryComponent
from indexing import Index, Posting
import merger_postings
from text import ProjectTokenProcessor
from queries import querycomponent
from indexing import DiskPositionalIndex

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
    # intersecting the resulting postings.
    def get_postings(self, index : Index, token_processor: ProjectTokenProcessor) -> list[Posting]:
        #merger_postings = and_merge

        result = [Posting]
        is_not = self.components[0].is_not

        posting1 = self.components[0].get_postings(index, token_processor)
        for i in range(1,len(self.components)):
            posting2 = self.components[i].get_postings(index, token_processor)

            if is_not: #so incase we have a negative posting just 1
                posting1 = merger_postings.and_not_merge(posting2, posting1)

            if self.components[i].is_not:
                posting1 = merger_postings.and_not_merge(posting1,posting2)

            else:
                posting1 = merger_postings.and_merge(posting1, posting2)
        #print(posting1)
        result = posting1
        return result

    def __str__(self):
        return " AND ".join(map(str, self.components))
