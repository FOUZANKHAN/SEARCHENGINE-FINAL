from pathlib import Path
from indexing import Index, PositionalInvIndex
from struct import *
from numpy import log as ln
from math import sqrt
import sqlite3

class DiskIndexWriter:

    def __init__(self,posindex: PositionalInvIndex, index_path: Path):
        self.index = posindex
        self.index_path = index_path
        self.posting_path = index_path/"postings.bin"
        self.doc_weight_path = index_path/"docWeights.bin"
        self.avg_tokens_path = index_path/"avg_token_corpus.bin"
        #self.doc_wights_path = index_path
        self._con = sqlite3.connect("bytepositions.db")
        self._cursor = self._con.cursor()
        self._cursor.execute("""CREATE TABLE if not exists termBytePositions (term text, byte_position integer)""")

    # def get_byte_position(self, term:str) -> int:
    #     self._cursor.execute("SELECT byte_position FROM termBytePositions WHERE term=:term",{'term': term})
    #     byte_pos = self._cursor.fetchone()
    #     return byte_pos[0] if byte_pos else -1  

    # def get_all_byte_positions(self):
    #     self._cursor.execute('SELECT * FROM termBytePositions')
    #     rows = self._cursor.fetchall()
    #     for row in rows:
    #         print(row)

    def write_docWeights(self, document_weights, docLengthd, byteSized, average_tftd):
        # Write Ld as an 8-byte double
        with open(self.doc_weight_path, 'wb') as f:
            for dw, dl, bs, atftd in zip(document_weights, docLengthd, byteSized, average_tftd):
                f.write(pack('>d', float(dw)))
                f.write(pack('>d', float(dl)))
                f.write(pack('>d', float(bs)))
                f.write(pack('>d', float(atftd)))

    def write_avg_tokens_corpus(self, document_tokens_length_average):
        # Write docLength average as an 8 byte double
        with open(self.avg_tokens_path, 'wb') as f:
            f.write(pack('>d', float(document_tokens_length_average)))
            
    def writeindex(self, posindex:PositionalInvIndex):
        self.index = posindex

        mode = 'wb' 
        with open(self.posting_path, mode) as file1:
        # Format for saving: dft, doc_id, tfd, pos1, pos2...
            vocab = self.index.vocabulary()#sorted vocab   
            byteposition = 0
            for term in vocab:
                self._cursor.execute("INSERT INTO termBytePositions VALUES (:term, :byte_position)",
                                         {'term': term, 'byte_position': byteposition})
                allpostings = self.index.get_postings(term) #postingq = [[2,[11,90,123]],[5,[45,90,128,129,158]],[6,[2,69]],[7,[12,151,180]]]
                dft = len(allpostings)
                file1.write(pack('>i',dft))
                byteposition += calcsize('>i')
                dummy_doc_id = 0#this is the preve docid
                for posting in allpostings: #[[2,[11,90,123]]]
                    ids_i = posting.doc_id - dummy_doc_id
                    file1.write(pack('>i',ids_i))
                    byteposition += calcsize('>i')
                    tft = len(posting.position_list)
                    file1.write(pack('>i',tft))
                    byteposition += calcsize('>i')
                    #wdt = 1 + ln(tft)
                    #file1.write(pack('>d',wdt))
                    #byteposition += calcsize('>d')
                    dummyposition = 0
                    for positions in posting.position_list:
                        position_i = positions-dummyposition #save the gaps
                        file1.write(pack('>i',position_i))
                        byteposition += calcsize('>i')
                        dummyposition = position_i     
                    dummy_doc_id = posting.doc_id
            
        
        self._con.commit()
        self._cursor.close()
            

        
        
    
   
   
   
