class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int):
        self.doc_id = doc_id
        self.position_list = []

    def __init__(self, doc_id : int, positions : list[int]):
        self.doc_id = doc_id
        self.position_list = positions
    

    def __str__(self)->str:
        return f"{self.doc_id}, {self.position_list}"

    def __repr__(self):
        return str(self)
