from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PositionalInvIndex
from text import ProjectTokenProcessor, EnglishTokenStream
from ranked_strategy import RankedStrategy,Trad,Default,Okapi,Wacky
from porter2stemmer import Porter2Stemmer
import time
from queries import *
from indexing import DiskPositionalIndex
from diskindexwriter import DiskIndexWriter
from numpy import log as ln
from math import sqrt
from heapq import nlargest

# def new_pos_index_corpus(corpus : DocumentCorpus) -> (Index):
#     document_weights = [] 
#     token_processor = ProjectTokenProcessor()
#     PosInvIndex = PositionalInvIndex(len(corpus))

#     for d in corpus:
#         term_tftd = {}
#         position = 1
#         stream = EnglishTokenStream(d.get_content())
#         for word in stream:
#             processed_term_array = token_processor.process_token(word)
#             for processed_term in processed_term_array:
#                 if processed_term:
#                     if processed_term not in term_tftd.keys():
#                         term_tftd[processed_term] = 0 #Initialization
#                     term_tftd[processed_term] += 1
#                     position += 1
#                     PosInvIndex.add_term(processed_term, d.id, position)
#         Ld = 0
#         for tftd in term_tftd.values():
#             wdt = 1 + ln(tftd)
#             wdt = wdt**2
#             Ld += wdt
#         Ld = sqrt(Ld)
#         document_weights.append(Ld)
                   
#     return PosInvIndex,document_weights

def new_pos_index_corpus(corpus:DocumentCorpus) -> (Index):
    token_processor = ProjectTokenProcessor()
    PosInvIndex = PositionalInvIndex(len(corpus))
    
    document_weights = []  # Ld for all documents in corpus
    document_tokens_length_per_document = []  # docLengthd - Number of tokens in a document
    document_tokens_length_total = 0  # total number of tokens in all the documents in corpus
    average_tftds = []  # ave(tftd) - average tftd count for a particular document
    byte_size_ds = []  # byteSized - number of bytes in the file for document d
    for d in corpus:
        #print("Processing the document: ", d.id)
        term_tftd = {}  # Term -> Term Frequency in a document
        stream = EnglishTokenStream(d.get_content())
        document_tokens_length_d = 0  # docLengthd - number of tokens in the document d
        position = 1
        for word in stream:
            processed_term_array = token_processor.process_token(word)
            for processed_term in processed_term_array:
                if processed_term:
                    if processed_term not in term_tftd.keys():
                        term_tftd[processed_term] = 0 #Initialization
                    term_tftd[processed_term] += 1
                    position += 1
                    PosInvIndex.add_term(processed_term, d.id, position)
            # number of tokens in document d
                    document_tokens_length_d += 1

        Ld = 0
        for tftd in term_tftd.values():
            wdt = 1 + ln(tftd)
            wdt = wdt ** 2
            Ld += wdt
        Ld = sqrt(Ld)
        document_weights.append(Ld)
        # docLengthd - update the number of tokens for the document
        document_tokens_length_per_document.append(document_tokens_length_d)
        # update the sum of tokens in all documents
        document_tokens_length_total = document_tokens_length_total + document_tokens_length_d
        total_tftd = 0
        average_tftd = 0
        for tf in term_tftd.values():
            total_tftd += tf
        # print("Total tftd and len(term_tftf) for doc d: ", d.get_file_name(), total_tftd, len(term_tftd))
        # Handling empty files
        if total_tftd == 0 or len(term_tftd) == 0:
            average_tftds.append(average_tftd)
        else:
            average_tftd = total_tftd / len(term_tftd)
            average_tftds.append(average_tftd)
        # byteSized - number of bytes in the file for document d
        byte_size_d = d.get_file_size()
        byte_size_ds.append(byte_size_d)

    # docLengthA - average number of tokens in all documents in the corpus
    document_tokens_length_average = document_tokens_length_total / len(corpus)
    return PosInvIndex, document_weights, document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average


def indexcreater(directoryname) -> Index:
    if directoryname == "MobyDick" or directoryname == "mobydick":
        print(f"Indexing {directoryname}")
        corpus_path = Path(directoryname)
        d = DirectoryCorpus.load_text_directory(corpus_path,".txt")
        localindex,localdocwt,document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average = new_pos_index_corpus(d)
    else:
        print(f"Indexing {directoryname}")
        corpus_path = Path(directoryname)
        d = DirectoryCorpus.load_json_directory(corpus_path,".json")
        localindex,localdocwt,document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average = new_pos_index_corpus(d)

    return localindex,d,localdocwt,document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average




if __name__ == "__main__":
    
    rasta = input("Give me the path to the directory\n>> ")
    index_path = Path(rasta)/Path("dat")
    #doc_weights_path = Path(rasta)/Path("dat")/Path("docWeights.bin")
    
    mode_select_instruct = int(input("1.Create Index\n2.Query Index\n>> "))
    
    mode = mode_select_instruct
    querying_style_selected = False
    
    parser = BooleanQueryParser()

    initial_indexing = True if int(mode) == 1 else False
    querying_mode = not initial_indexing
    strategyMap = {1: Default, 2: Trad, 3: Okapi, 4: Wacky}
    
    while True:
        if initial_indexing:
            user_directory_path = input("Enter the the directory you want to index\n>> ")
            st = time.time()
            projectindex, d,localdocwt,document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average = indexcreater(user_directory_path)
            #print(projectindex)
            et = time.time()
            elapsedtime = et-st
            print(f'Indexing took {elapsedtime} seconds')
            index_path = user_directory_path/Path("dat")

            #this is creating the Disk Index Writer
            diskindexwriterobject = DiskIndexWriter(projectindex, index_path)
            diskindexwriterobject.writeindex(projectindex)
            diskindexwriterobject.write_docWeights(localdocwt,document_tokens_length_per_document,byte_size_ds,average_tftds)
            diskindexwriterobject.write_avg_tokens_corpus(document_tokens_length_average)
            
            diskpositionalindex = DiskPositionalIndex(index_path)
            initial_indexing = False
            
        else:
            d = DirectoryCorpus.load_json_directory(rasta,".json")
            corpus_size = len(d)
            diskpositionalindex = DiskPositionalIndex(index_path)
            try:
                query_mode = int(input("1.Boolean Mode\n2.Ranked Mode\n>> "))
            except ValueError:
                print("Please select from these options")
            
            
            if query_mode == 1:
                query = input("\n(mode 1) Please enter the words to search: ")
                querytosearch = query.split()
                if query.startswith(":q"):
                    print("\n Exiting the program")
                    exit()
                
                elif ":stem" in querytosearch:
                    stemmer = Porter2Stemmer()
                    print(stemmer.stem(querytosearch[1]))
                
                elif query.startswith(":vocab"):  
                    ans = projectindex.vocabulary()
                    numberofterms = len(ans)
                    for i in range(1000):
                        print(f'\n {ans[i]}')
                    print(f'The number of terms is {numberofterms}')
                
                elif ":index" in querytosearch:
                    pass #not implemented 
                
                elif ":mode" in querytosearch:
                    mode_select_instruct = int(querytosearch[1])
                else:
                    q = parser.parse_query(query)
                    
                    list_docids =[]
                    numberth = 1
                    allpostings = q.get_postings(diskpositionalindex,ProjectTokenProcessor)
                    #print(allpostings)
                    #THE DISKPOSITIONAL INDEX PHRASE? NEAR HAS TO BE FIXED BEFORE

                    for posting in allpostings:
                        ##print(posting)
                        doc = d.get_document(posting.doc_id)
                        list_docids.append(posting.doc_id)
                        print(f"\n {numberth}.Doc Title: {doc.title}")
                        numberth +=1
                        #print(f"{posting}")
                    print(f"\n Number of documents that have the term '''{query}''' are {len(list_docids)}")

                    user_read = input("\n Would you like to read the contents of any file? (Y/y) or press anything to continue: \n")
                    if user_read == "Y" or user_read == "y":
                        if list_docids:
                            doc_num = int(input("\nEnter Document Number to view content: "))
                            print("Document contents are: ")
                            doc_read = d.get_document(list_docids[doc_num-1])
                            for s in doc_read.get_content():
                                print(s)
                    else:
                        pass
            else:
                print("You are in ranked mode")
                query = input("\n(mode 2) Please enter the words to rank: ")
                print("\nChoose a ranking strategy:")
                print("1. Default")
                print("2. Traditional(tf-idf)")
                print("3. Okapi BM25")
                print("4. Wacky")
                choice = input(">> ")
                strategy = strategyMap.get(int(choice))
                rankedStrategy = RankedStrategy(strategy)
                #corpus_size = 36803#kinda hardcoding it

                accumulator = rankedStrategy.calculate(corpus_size,query,diskpositionalindex)
                
                print()
                print("*"*80)
                K = 10
                heap = [(score, doc_id) for doc_id, score in accumulator.items()]
                print(f"Top {K} documents for query: {query}")
                for k_documents in nlargest(K, heap):
                    score, doc_id = k_documents
                    print(f"Doc Title: {d.get_document(doc_id).title}, Score: {round(score,4)}")

               
               


                