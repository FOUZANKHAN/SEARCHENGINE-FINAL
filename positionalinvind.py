from pathlib import Path
from xxlimited import new
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex,InvertedInd, PositionalInvIndex
from text import BasicTokenProcessor, EnglishTokenStream
import time

def new_pos_index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    #vocabulary = set()
    #pro = [
    PosInvIndex = PositionalInvIndex(len(corpus))

    for d in corpus:
        position = 0
        stream = EnglishTokenStream(d.get_content())
        for word in stream:
            processed_term = token_processor.process_token(word)
            position += 1
            PosInvIndex.add_term(processed_term, d.id, position)
    return PosInvIndex

if __name__ == "__main__":
    st = time.time()
    user_path = input("Enter the the directory you'd like to search ")
    corpus_path = Path(user_path)
    
    d = DirectoryCorpus.load_json_directory(corpus_path,".json")
    secondindex = new_pos_index_corpus(d)
    #print(secondindex)
    et = time.time()
    elapsedtime = et-st
    marker = True
    while(marker):
        querytosearch = input("Please enter the word to search or type quit to close: ")
        if(querytosearch == "quit" or querytosearch == "Quit"):
            marker = False
            print("Quiting.....")
        else:
            try:
                c = 0
                for postings in secondindex.get_postings(querytosearch):
                    c+=1
                    print(f"Document ID {postings.doc_id}") ##
                    doc = d.get_document(postings.doc_id)
                    print(f"Doc Title: {doc.title}")
                print(f'{elapsedtime} seconds')
                print(f'{c} documents have the term:  {querytosearch}')
            except TypeError:
                print(f'The word {querytosearch} was not found')

#FOUZAN KHAN POSITIONAL INVERTED INDEX SEPT15th 3pm