
import os
from typing import List
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings



def get_chatbot_response(model_name,messages,temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append(message)
    
    llm = ChatGroq(
        model=os.getenv("MODEL_NAME",model_name) ,
        temperature=temperature,
        max_tokens=2000,
        timeout=None,
        max_retries=2,
    )
    
    response = llm.invoke(input_messages)
    
    return response.content

def get_embeddings(texts:List[str]):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf_embeddings = HuggingFaceBgeEmbeddings(
        model_name=os.getenv("EMBEDDINGS_MODEL_NAME"),
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    embeddings_output = hf_embeddings.embed_documents(texts=texts)
    
    return embeddings_output
    

def double_check_json_output(json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(model_name=os.getenv("MODEL_NAME"),messages=messages)

    return response