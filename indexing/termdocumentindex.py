from bisect import bisect_left
from decimal import InvalidOperation
from pydoc import doc
from typing import Iterable
from . import Posting, Index


class TermDocumentIndex(Index):
    """Implements an Index using a term-document matrix. Requires knowing the full corpus
    vocabulary and number of documents prior to construction."""

    def __init__(self, vocab : Iterable[str], corpus_size : int):
        """Constructs an empty index using the given vocabulary and corpus size."""
        self.vocabulary = list(vocab)
        self.vocabulary.sort()
        self.corpus_size = corpus_size
        self._matrix = [[False] * corpus_size for _ in range(len(vocab))]

    def add_term(self, term : str, doc_id : int):
        """Records that the given term occurred in the given document ID."""
        # bisect_left does a binary search to find where the given item would be in the list, if it is there.
        vocab_index = bisect_left(self.vocabulary, term)
        # Check to make sure the term is actually in the list.
        if vocab_index != len(self.vocabulary) and self.vocabulary[vocab_index] == term:
            self._matrix[vocab_index][doc_id] = True
        else:
            raise InvalidOperation("Cannot add a term that is not already in the matrix")

    def get_postings(self, term : str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the giventerm."""
        docsthathavethem = []
        something = bisect_left(self.vocabulary, term)
        #print(self._matrix[something])
        if something != len(self.vocabulary) and self.vocabulary[something] == term:
            for i in range(len(self._matrix[something])):
                if self._matrix[something][i] == True:
                    docsthathavethem.append(Posting(i))
            return docsthathavethem

        # TODO: implement this method.
		# Binary search the self.vocabulary list for the given term. (see bisect_left, above)
		# Walk down the self._matrix row for the term and collect the document IDs (column indices)
		# of the "true" entries.

    def vocabulary(self) -> Iterable[str]:
        return self.vocabulary

 #prints the entire matrix
    def __str__(self) -> str:
        return str(self._matrix)
