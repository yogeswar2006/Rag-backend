
        
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import SecretStr



def RagSearch(retrieved_docs,query):
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key is None:
       raise ValueError("GROQ_API_KEY not found in environment variables")
    llm = ChatGroq(api_key=SecretStr(groq_api_key), model="llama-3.3-70b-versatile",temperature=0.1,max_tokens=1024)
    
    if not retrieved_docs:
        return "No relevant documents found to answer the query."
    
    # Step 2: Prepare context for LLM
    context = "\n\n".join([f"Document {doc['metadata'].get('doc_index', 'N/A')}:\n{doc['content']}" for doc in retrieved_docs])
    
    # Step 3: Generate answer using LLM
    prompt = f"Based on the following retrieved documents, answer the question:\n\n Context:{context}\n\nQuestion: {query}\nAnswer:"
    
    try:
        response = llm.invoke([prompt.format(context=context,query=query)])
        return response.content
    except Exception as e:
        print(f"Error generating answer with LLM: {e}")
        return "Error generating answer."
