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
    user_directory_path = input("Enter the the directory you want to index\n>> ")
    st = time.time()
    #mode_select_instruct = int(input("1.Create Index\n2.Query Index\n>> "))
    projectindex, d,localdocwt,document_tokens_length_per_document, byte_size_ds, average_tftds, document_tokens_length_average = indexcreater(user_directory_path)
    et = time.time()
    elapsedtime = et-st
    print(f'Indexing took {elapsedtime} seconds')
    diskindexwriterobject = DiskIndexWriter(projectindex, index_path)
    diskindexwriterobject.writeindex(projectindex)
    diskindexwriterobject.write_docWeights(localdocwt,document_tokens_length_per_document,byte_size_ds,average_tftds)
    diskindexwriterobject.write_avg_tokens_corpus(document_tokens_length_average)        
    diskpositionalindex = DiskPositionalIndex(index_path)
    
    strategyMap = {1: Default, 2: Trad, 3: Okapi, 4: Wacky}
    parser = BooleanQueryParser()
    
    f = open(Path("relevance_check/queries-list"), "r")
    queries = f.readlines()
    print(queries)
    f.close()

    f1 = open(Path("relevance_check/qrel"), "r")
    relevantfiles = f1.readlines()
    f1.close()
        
    for i in range(0,len(queries)):
        q = parser.parse_query(queries[i])
        #relevant docids for query 1 to 5
        relevantfile = relevantfiles[i].split()
        checkrel= []
        for j in range(0,len(relevantfile)):
            relevantfile[j] = int(relevantfile[j])
            checkrel.append(relevantfile[j])

        #print(checkrel) has all  the relevant document titles
        
        print(f"******{queries[i]}********")
        list_docids =[]
        numberth = 1
        allpostings = q.get_postings(diskpositionalindex,ProjectTokenProcessor)
        #print(allpostings)
        #THE DISKPOSITIONAL INDEX PHRASE? NEAR HAS TO BE FIXED BEFORE
        query_returneddocs_names = []
        booval = []
        for posting in allpostings:
            ##print(posting)
            doc = d.get_document(posting.doc_id)
            list_docids.append(posting.doc_id)
            print(f"\n {numberth}.Doc Title: {doc.title}")
            #query_returneddocs_names.append(int(doc.get_file_name()))
            #print(f"{doc.get_file_name()}")
            numberth +=1
            #print(f"{posting}")
        print(f"{query_returneddocs_names}")
        print(f"\n Number of documents that have the term '''{queries[i]}''' are {len(list_docids)}")

        
        #default for all 5 queries  
        strategy = strategyMap.get(1)
        rankedStrategy = RankedStrategy(strategy)
        corpus_size = 236#kinda hardcoding it

        accumulator = rankedStrategy.calculate(corpus_size,queries[i],diskpositionalindex)

        print("*"*80)
        K = 50
        heap = [(score, doc_id) for doc_id, score in accumulator.items()]
        print(f"Top {K} documents for query: {queries[i]}")
        prec = []
        relevance = 1
        sum = 0
        for k_documents in nlargest(K, heap):
            score, doc_id = k_documents
            print(f"Doc Title: {d.get_document(doc_id).title}, Score: {score}")
            docq = d.get_document(doc_id)
            query_returneddocs_names.append(int(doc.get_file_name()))
            for i in range(len(checkrel)):
                if(query_returneddocs_names[i] in checkrel):
                    relevance += 1
                    precision = relevance/(i+1)
                    sum += precision
                    prec.append(precision)
                else:
                    try:
                        prec.append(relevance/(i+1))
                    except ZeroDivisionError:
                        prec.append(0)
        print(prec)

                