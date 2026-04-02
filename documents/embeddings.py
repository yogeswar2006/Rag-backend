from typing import List,Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np

class Embeddings():
    
    def __init__(self,model_name:str = "all-MiniLM-L6-v2"):
        """Constructer for Loading model for chunking"""
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Loading sentenceTransformer model to convert chunks into vectors"""
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Successfully Loaded {self.model_name} . Dimension : {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error at loding model {self.model_name}")
            raise
        
    
    def generate_embeddings(self,texts:List[str]) -> np.ndarray:
         """Generating embeddings for provided texts"""
         if not self.model:
             raise  ValueError("Model not loaded")
         
         print(f"generating embeddings for {len(texts)}")
         embeddings = self.model.encode(texts,show_progress_bar=True)
         print(f"Generated embeddings for {len(texts)}")
         return embeddings
         
    
    def Split_generation(self,documents:List[Any],chunk_size=1000,chunk_overlap=200):
        """Texts to smaller chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,  
            length_function = len,
            separators=['\n\n','\n',' ',''],
        )
        split_docs = text_splitter.split_documents(documents)
        print(f"Splitted {len(documents)} to {len(split_docs)}")
        return split_docs