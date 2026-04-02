from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
import os
from pathlib import Path



def Load_Documents(saved_docs):
   
    all_documents=[]
    
 
    for doc_obj in saved_docs:
        file_path = doc_obj.file.path  #  correct path

        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

        for d in documents:
            d.metadata["author"] = "Yogi"
            d.metadata["file_type"] = "pdf"

        all_documents.extend(documents)

        print(f"Loaded pdf file: {doc_obj.file.name}")

    print(f"Loaded total {len(saved_docs)} pdf files")

    return all_documents 
    
    # for Excel_loader
    # xl_file_paths = list(dir.glob("**/*.xlsx"))  
    # for file in xl_file_paths:
    #     loader= UnstructuredExcelLoader(str(file))
    #     document = loader.load()
    #     for doc in document:
    #         doc.metadata["file_type"]="xlsx"
    #         doc.metadata["author"]="Yogi"
    #     all_documents.extend(document)
    #     print(f"Loaded xlsx file :{file.name}")
    # print(f"Loaded total {len(xl_file_paths)} xlsx files")
       # # for text_loader
    # text_file_paths = list(dir.glob("**/*.txt"))
    # for file in text_file_paths:
    #     loader = TextLoader(str(file))
    #     document = loader.load()
    #     for doc in document:
    #         doc.metadata["author"]="Yogi"
    #         doc.metadata["file_type"]="text"
    #     all_documents.extend(document)
    #     print(f"Loaded text file :{file.name} ")
    # print(f"Loaded total {len(text_file_paths)} text files")
    
    # for pdf_loader
    
    
    
   
    