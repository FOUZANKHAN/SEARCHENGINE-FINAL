from abc import ABC
from math import sqrt
from numpy import log as ln
from queries import TermLiteral
from text import ProjectTokenProcessor
from indexing import DiskPositionalIndex

class RankedStrategy(ABC):
    def __init__(self, strategy):
        self._strategy = strategy

    def calculate(self,corpus_size,query,disk_index) -> {}:
        return self._strategy.calculate(self,corpus_size=corpus_size,query=query,disk_index = disk_index)

class Default():

    def calculate(self,corpus_size,query,disk_index):
        accumulator = {}
        N = corpus_size
        #token_processor = ProjectTokenProcessor()
        #print(N)

        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index,ProjectTokenProcessor)
            
            dft = len(postings)
            #if dft != 0:
            wqt = ln(1 + N / dft)
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            for posting in postings:
                wdt = 1 + ln(posting.position_list)
                if posting.doc_id not in accumulator.keys():
                    accumulator[posting.doc_id] = 0.
                accumulator[posting.doc_id] += (wdt * wqt)

        for doc_id in accumulator.keys():
            Ld = disk_index.get_doc_info(doc_id, "Ld")
            accumulator[doc_id] /= Ld

        return accumulator
        
class Trad():
    def calculate(self, corpus_size, query, disk_index):
        accumulator = {}
        N = corpus_size
        #token_processor = ProjectTokenProcessor()

        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index, ProjectTokenProcessor)
            dft = len(postings)
            if dft != 0:
                wqt = ln(N / dft)
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            for posting in postings:
                wdt = posting.position_list #tfidf term frequecu basically
                if posting.doc_id not in accumulator.keys():
                    accumulator[posting.doc_id] = 0.
                accumulator[posting.doc_id] += (wdt * wqt)

        for doc_id in accumulator.keys():
            Ld = disk_index.get_doc_info(doc_id, "Ld")
            accumulator[doc_id] /= Ld

        return accumulator

class Okapi():
    def calculate(self, corpus_size,query,disk_index):
        accumulator = {}
        N = corpus_size
        #token_processor = ProjectTokenProcessor()

        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index, ProjectTokenProcessor)
            dft = len(postings)
            if dft != 0:
                wqt = max(0.1, ln((N - dft + 0.5) / (dft + 0.5)))
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            for posting in postings:
                docLength = disk_index.get_doc_info(posting.doc_id, "docLength")
                doc_tokens_len_avg = disk_index.get_avg_tokens()#problem
                denominator = (1.2 * (0.25 + (0.75 * (docLength / doc_tokens_len_avg)))) + posting.position_list
                wdt = (2.2 * posting.position_list) / denominator

                if posting.doc_id not in accumulator.keys():
                    accumulator[posting.doc_id] = 0.
                accumulator[posting.doc_id] += (wdt * wqt)

        for doc_id in accumulator.keys():
            Ld = 1
            accumulator[doc_id] /= Ld

        return accumulator

class Wacky():
    def calculate(self,corpus_size,query,disk_index):
        accumulator = {}
        N = corpus_size
        #token_processor = ProjectTokenProcessor()
        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index, ProjectTokenProcessor)
            
            dft = len(postings)
            if dft != 0:
                wqt = max(0, ln((N - dft) / dft))
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            for posting in postings:
                average_tftd = disk_index.get_doc_info(posting.doc_id, "avg_tftd")#problem
                wdt = (1 + ln(posting.position_list)) / (1 + ln(average_tftd))
                if posting.doc_id not in accumulator.keys():
                    accumulator[posting.doc_id] = 0.
                accumulator[posting.doc_id] += (wdt * wqt)

        for doc_id in accumulator.keys():
            byte_size = disk_index.get_doc_info(doc_id, "byte_size")
            Ld = sqrt(byte_size)
            accumulator[doc_id] /= Ld

        return accumulator

class Default_v():

    def calculate(self,corpus_size,query,disk_index):
        accumulator = {}
        N = corpus_size
        #token_processor = ProjectTokenProcessor()
        #print(N)
        #MAP 1.4 highest MAP
        thres = 1.4
        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index,ProjectTokenProcessor)
            
            dft = len(postings)
            #if dft != 0:
            wqt = ln(1 + N / dft)
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            if wqt>thres:
                for posting in postings:
                    wdt = 1 + ln(posting.position_list)
                    if posting.doc_id not in accumulator.keys():
                        accumulator[posting.doc_id] = 0.
                    accumulator[posting.doc_id] += (wdt * wqt)

                for doc_id in accumulator.keys():
                    Ld = disk_index.get_doc_info(doc_id, "Ld")
                    accumulator[doc_id] /= Ld

        return accumulator


class Wacky_v():
    def calculate(self,corpus_size,query,disk_index):
        accumulator = {}
        N = corpus_size
        thres = 1.0
        
        for term in set(query.split(" ")):
            tokenized_term = TermLiteral(term, False)
            postings = tokenized_term.get_postings(disk_index, ProjectTokenProcessor)
           
            dft = len(postings)
            if dft != 0:
                wqt = max(0, ln((N - dft) / dft))
            #print(f"\n{dft} postings for the term {term}; with wQt = {wqt}")
            if wqt > thres:
                for posting in postings:
                    average_tftd = disk_index.get_doc_info(posting.doc_id, "avg_tftd")#problem
                    wdt = (1 + ln(posting.position_list)) / (1 + ln(average_tftd))
                    if posting.doc_id not in accumulator.keys():
                        accumulator[posting.doc_id] = 0.
                    accumulator[posting.doc_id] += (wdt * wqt)

                for doc_id in accumulator.keys():
                    byte_size = disk_index.get_doc_info(doc_id, "byte_size")
                    Ld = sqrt(byte_size)
                    accumulator[doc_id] /= Ld

        return accumulator