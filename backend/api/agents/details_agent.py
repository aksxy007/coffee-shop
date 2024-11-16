from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response,get_embeddings
from pinecone import Pinecone

load_dotenv()


class DetailsAgent():
    def __init__(self) -> None:
        self.model_name = os.getenv("MODEL_NAME")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
    
    
    def get_closest_results(self,input_embeddings,top_k=2):
        index = self.pc.Index(self.index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )
        
        return results
        
    def get_response(self,messages):
        messages = deepcopy(messages)
        
        user_message = messages[-1]['content']
        query_embeddings = get_embeddings(texts=[user_message])[0]
        result = self.get_closest_results(query_embeddings)
        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in result['matches'] ])
        
        user_prompt = f"""
            Using the given contexts below, answer the query.
            
            contexts:
            {source_knowledge}
            
            query: {user_message}
        """
        
        system_prompt = """
            You are a customer support agent for a coffee shop called Merry's way. 
            You should answer every question as if you are waiter and provide the neccessary information to the user regarding their orders.
            If the query says no thanks , say thank you.
            Do not recommend anything thing from your side.
        """
        
        messages[-1]['content'] = user_prompt
        input_messages=[{"role":"system","content":system_prompt}]+messages[-3:]
        
        chatbot_response = get_chatbot_response(self.model_name,messages=input_messages)
        print(chatbot_response)
        output = self.postprocess(chatbot_response)
        
        return output
    
    def postprocess(self,output):
    
        dict_output = {
            "role": "assistant",
            "content": output,
            "memory": {"agent":"details_agent",
                       
                      }
        }
        
        return dict_output