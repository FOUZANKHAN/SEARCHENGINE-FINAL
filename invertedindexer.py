from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex
from indexing import InvertedInd
from text import BasicTokenProcessor, EnglishTokenStream
import time


def new_index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    #vocabulary = set()
    #pro = [
    InvIndex = InvertedInd(len(corpus))
    for d in corpus:
        stream = EnglishTokenStream(d.get_content())
        for word in stream:
            processed_term = token_processor.process_token(word)
            InvIndex.add_term(processed_term, d.id)
            #InvIndex.get_vocabulary(processed_term)
    return InvIndex

if __name__ == "__main__":
    #corpus_path = Path("../jsonfiles")
    st = time.time()
    corpus_path = Path("jsonfiles")
    #corpus_path = Path()
    #d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    d = DirectoryCorpus.load_json_directory(corpus_path,".json")
    secondindex = new_index_corpus(d)
    print(secondindex)
    et = time.time()
    elapsedtime = et-st
    marker = True
    while(marker):
        querytosearch = input("Please enter the word to search or type quit to close: ")
        if(querytosearch == "quit" or querytosearch == "Quit"):
            marker = False
            print("Exiting.....")
        else:
            c = 0
            for docids in secondindex.get_postings(querytosearch):
                c+=1
                print(f"Document ID {docids.doc_id}") ##
                doc = d.get_document(docids.doc_id)
                print(f"Doc Title: {doc.title}")
            print(f'{elapsedtime} seconds')
            print(f'{c} documents have the term {querytosearch}')
