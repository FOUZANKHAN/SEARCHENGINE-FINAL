from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex
from indexing import InvertedInd
from text import BasicTokenProcessor, EnglishTokenStream
#THIS IS VERSION OF MY TERMDOCUMENT INDEX FILE
"""This basic program builds a term-document matrix over the .txt files in
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:

    token_processor = BasicTokenProcessor()
    vocabulary = set()
    for d in corpus:
        #print(f"Found document {d.title}")
        stream = EnglishTokenStream(d.get_content()) #this makes stream for each document available to us
        for word in stream:
            term = token_processor.process_token(word)
            vocabulary.add(term)
    #print(vocabulary)

    Index = TermDocumentIndex(vocabulary,len(corpus))
    for d in corpus:
        streame = EnglishTokenStream(d.get_content())
        for w in streame:
            processedterm = token_processor.process_token(w)
            Index.add_term(processedterm,d.id)
    return Index



def new_index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    #vocabulary = set()
    #pro = []
    len_corpus = 9
    InvIndex = InvertedInd(len_corpus)
    for d in corpus:
        stream = EnglishTokenStream(d.get_content())
        for word in stream:
            processed_term = token_processor.process_token(word)
            InvIndex.add_term(processed_term, d.id)
    return InvIndex

    # TODO:
        #   Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        #   Iterate through the token stream, processing each with token_processor's process_token method.
        #   Add the processed token (a "term") to the vocabulary set.

    # TODO:
    # After the above, next:
    # Create a TermDocumentIndex object, with the vocabular you found, and the len() of the corpus.
    # Iterate through the documents in the corpus:
    #   Tokenize each document's content, again.
    #   Process each token.
    #   Add each processed term to the index with .add_term().

if __name__ == "__main__":
    corpus_path = Path("MobyDick10Chapters")
    d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")

    #Build the index over this directory.
    index = index_corpus(d)
    print(index)

    #secondindex = new_index_corpus(d)
    #print(secondindex)

    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.


    marker = True
    while(marker):
        querytosearch = input("Please enter the word to search or type exit to close: ")
        if(querytosearch == "exit" or querytosearch == "Exit"):
            marker = False
            print("Exiting.....")
        else:
            for docids in index.get_postings(querytosearch):
                #print(f"Document ID {p.doc_id}") ##
                doc = d.get_document(docids.doc_id)
                print(f"Doc Title: {doc.title}")


    # TODO: fix this application so the user is asked for a term to search.
