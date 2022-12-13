from pathlib import Path
from typing import Iterable
from . import Posting, Index,PositionalInvIndex
from diskindexwriter import DiskIndexWriter
from struct import unpack
import sqlite3

class DiskPositionalIndex(Index):
    
    def __init__(self, index_path: Path):

        self.posting_disk_path = index_path/"postings.bin" #this is valru = jsonsample/dat/postings.bin
        self.doc_weight_path = index_path/"docWeights.bin"#this is supposed to be docWeights.bin
        self.avg_tokens_path = index_path/"avg_token_corpus.bin"

    def get_byte_position(self, term:str) -> int:
        self._con = sqlite3.connect("bytepositions.db")
        self._cursor = self._con.cursor()
        self._cursor.execute("SELECT byte_position FROM termBytePositions WHERE term=:term",{'term': term})
        byte_pos = self._cursor.fetchone()
        #self._cursor.close()
        return byte_pos[0] if byte_pos else -1 
    
    def get_doc_info(self, doc_id: int, doc_info: str) -> float:
        doc_info_dict = {"Ld": 0, "docLength": 1, "byte_size": 2, "avg_tftd": 3}
        num_bytes = 8
        start_byte_position = doc_id * 32 + (doc_info_dict[doc_info] * num_bytes)
    
        with open(self.doc_weight_path, "rb") as f:
            f.seek(start_byte_position)
            doc_param = unpack(">d", f.read(num_bytes))[0]
        return doc_param

    def get_avg_tokens(self) -> float:
        with open(self.avg_tokens_path, 'rb') as f:
            avg_tokens_length = unpack(">d", f.read(8))[0]
        return avg_tokens_length
    
    # def get_all_byte_positions(self):
    #      self._cursor.execute('SELECT * FROM termBytePositions')
    #      rows = self._cursor.fetchall()
    #      for row in rows:
    #          print(row)
    
    def get_postings(self, term: str) -> list[Posting]:
            start_byte_position = self.get_byte_position(term)
            postings = []
            # flag = True
            if start_byte_position != -1:
                num_bytes = 4
                mode = "rb"
                with open(self.posting_disk_path, mode) as f:
                    f.seek(start_byte_position)
                    dft = unpack('>i',f.read(num_bytes))[0]
                    prev_doc = 0
                
                    for _ in range(dft):
                        doc_id = unpack('>i',f.read(num_bytes))[0]
                        doc_id += prev_doc
                        tftd = unpack('>i',f.read(num_bytes))[0]
                        #wdt = unpack('>d',f.read(8))[0]
                        count = 0
                        #prevposition = 0
                        #positionallist = []
                        while count < tftd:
                            position = unpack('>i',f.read(num_bytes))[0]
                            count += 1   
                        prev_doc = doc_id
                        #posting = Posting(doc_id,tftd)
                        posting = Posting(doc_id,tftd)
                        postings.append(posting)
                #PROBLEM WITH THIS IS I DONT HAVE ANYTHING IN POSTING AS TFTD AND ITS NAMING THEM POSITIONS T000
                #f.close()
                if postings:
                    #print(f"diskposit {postings}")
                    return postings
    
    # def get_wdt(self, term: str) -> list[Posting]:
    #         start_byte_position = self.get_byte_position(term)
    #         postings = []
    #         # flag = True
    #         if start_byte_position != -1:
    #             num_bytes = 4
    #             mode = "rb"
    #             with open(self.index_disk_path, mode) as f:
    #                 f.seek(start_byte_position)
    #                 dft = unpack('>i',f.read(num_bytes))[0]
    #                 prev_doc = 0
                
    #                 for _ in range(dft):
    #                     doc_id = unpack('>i',f.read(num_bytes))[0]
    #                     doc_id += prev_doc
    #                     tftd = unpack('>i',f.read(num_bytes))[0]
    #                     wdt = unpack('>d',f.read(8))[0]
    #                     count = 0
    #                     #prevposition = 0
    #                     #positionallist = []
    #                     while count < tftd:
    #                         position = unpack('>i',f.read(num_bytes))[0]
    #                         count += 1   
    #                     prev_doc = doc_id
    #                     #posting = Posting(doc_id,tftd)
    #                     posting = Posting(doc_id,wdt)
    #                     postings.append(posting)
    #             #PROBLEM WITH THIS IS I DONT HAVE ANYTHING IN POSTING AS TFTD AND ITS NAMING THEM POSITIONS T000
    #             #f.close()
    #             if postings:
    #                 return postings

    
    def get_positional_postings(self, term: str) -> list[Posting]:
        #print(term)
        start_byte_position = self.get_byte_position(term)
        postings = []
        if start_byte_position != -1:
            num_bytes = 4
            mode = "rb"
            with open(self.posting_disk_path, mode) as f:
                f.seek(start_byte_position)
                dft = unpack('>i',f.read(num_bytes))[0]
                prev_doc = 0
                for _ in range(dft):
                    doc_id = unpack('>i',f.read(num_bytes))[0]
                    doc_id += prev_doc
                    tftd = unpack('>i',f.read(num_bytes))[0]
                    count = 0
                    prevposition = 0
                    positionallist = []
                    while count < tftd:
                        position = unpack('>i',f.read(num_bytes))[0]
                        actualposition = position + prevposition
                        prevposition = position
                        positionallist.append(actualposition)
                        count += 1   
                    prev_doc = doc_id
                    posting = Posting(doc_id,positionallist)
                    postings.append(posting)
            f.close()
        return postings
    
    # def get_doc_wt(self,docid:int) -> float:
    #     num_byts = 8
    #     mode = "rb"
    #     start_byte_pos = docid * num_byts
    #     with open(self.doc_weight_path,mode) as f:
    #         f.seek(start_byte_pos)
    #         ld = unpack('>d',f.read(num_byts))[0]
    #     f.close()
    #     return ld
    
    

 
