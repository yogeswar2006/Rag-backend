from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct
from dotenv import load_dotenv
load_dotenv()
import os
from typing import List ,Any
import numpy as np
import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.models import PayloadSchemaType


class VectorStore:
    
    def __init__(self,collection_name:str="Rag_Bot",vector_size:int=384):
        """Initializeing the collection in Qdrant"""
        self.collection_name = collection_name
        self.client  = QdrantClient(
            url=os.getenv("CLUSTER_ENDPOINT"),
            api_key=os.getenv("CLUSTER_API")
        )
        self.vector_size = vector_size
        
        
        self._initialize_QdrantClinet()
    
    def _initialize_QdrantClinet(self):
        
       try:
        self.client.get_collection(self.collection_name)
        print(f" Using existing collection: {self.collection_name}")
       except Exception:
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
        print(f" Created collection: {self.collection_name}")
       
       try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="company_id",
                field_schema=PayloadSchemaType.KEYWORD
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="user_id",
                field_schema=PayloadSchemaType.KEYWORD
            )

            print("Payload indexes ensured (company_id, user_id)")

       except Exception as e:
             print(f"Index creation warning (may already exist): {e}")
        
    def add_documents(self,documnets:List[Any],embeddings:np.ndarray,metadata:dict):
        
        """For adding all document and their embeddings into Qdrant cloud"""
        if (len(documnets)!=len(embeddings)):
            raise ValueError("documnets and embeddings count not matched!")
        points =[]
        for i,(doc,embedding) in enumerate(zip(documnets,embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        **(doc.metadata or {}),
                        "content":doc.page_content,
                        "user_id":metadata.get("user_id"),
                        "company_id":metadata.get("company_id"),
                        "doc_index":i
                    }
                )
            )
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Successfully Added {len(points)} documents to Qdrant Cloud")
        
    def Search(self,query:str,top_k:int,embedding,company_id:str):
            query_embedding = embedding.generate_embeddings([query])[0]
            
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                query_filter=Filter(   #  use Filter object
                  must=[
                   FieldCondition(
                       key="company_id",
                       match=MatchValue(value=str(company_id))
                   )
                   ]
                )
                
            )
            
            documents =[]
            for doc in results.points:
                
                if doc.payload is None:
                    payload = {}
                else:
                    payload = doc.payload 
                
                documents.append({
                    "score": doc.score,
                    "content":payload.get("content","No content found"),
                    "metadata":payload,
                    
                    
                })
            return documents