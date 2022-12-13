from .tokenprocessor import TokenProcessor
from porter2stemmer import Porter2Stemmer
import re
import string

class ProjectTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters
    from the token, and converting it to all lowercase."""
    #handlenumber_re = re.compile(r"^\W+|\W+$")
    #whitespace_re = re.compile(r"\W+")

    def process_token(self, token : str) -> str:
        stemmer = Porter2Stemmer()
        token_list = []
        #final_tokenized_list = []
        token = re.sub(r"^\W+|\W+$", "", token).lower()
        token = re.sub( '"',' ', token)
        if "-" in token:
            words = token.split('-')
            for word in words:
                token_list.append(word)
            token = token.replace('-','')
        token_list.append(token)

        token_list = map(stemmer.stem,token_list)
        
        #print(f"Process Token This is called and returns this to the {list(map(str,token_list))}")
        finallist = list(map(str,token_list))
        
        return finallist



    def process_query(self, token :str) -> str:
        stemmer = Porter2Stemmer()
        token = re.sub(r"^\W+|\W+$", "", token).lower()
        token = re.sub('"', '', token)
        token = map(stemmer.stem,token)
        return token
