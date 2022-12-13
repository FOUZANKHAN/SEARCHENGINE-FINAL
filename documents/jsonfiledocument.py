from pathlib import Path
from typing import Iterable
from .document import Document
from io import StringIO
import json

class JsonFileDocument(Document):
    """
    Represents a document that is saved as a simple text file in the local file system.
    """
    def __init__(self, id : int, path : Path):
        super().__init__(id)
        self.path = path

    def get_file_size(self) -> int:
        return self.path.stat().st_size
    
    def get_file_name(self) -> str:
        return self.path.stem
    #https://stackoverflow.com/questions/31890341/clean-way-to-get-the-true-stem-of-a-path-object

    
    
    @property
    def title(self) -> str:
        with open(self.path, 'r') as f:
             json_title = json.load(f)['title']
             return json_title

    # returns
    def get_content(self) -> Iterable[str]:
        with open(self.path, 'r') as f:
             file = StringIO(json.load(f)['body'])
             return file
             #file.truncate()
    

    def get_everything(self) -> Iterable[str]:
        with open(self.path,'r') as f:
            contents = f.read()
            print(contents)

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a TextFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)
