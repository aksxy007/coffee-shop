from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from .utils import get_chatbot_response

load_dotenv()


class GaurdAgent():
    def __init__(self) -> None:
        self.model_name = os.getenv("MODEL_NAME")
        
    def get_response(self,messages):
        messages = deepcopy(messages)
        
        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
            2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. ASk about recommendations of what to buy.
            5. Anything about you. 
            
            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menue item.
            
            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the points above and see if the message lies under thses points or not. Then you write some your thoughts about what point is the user message relevant to.
            "decision": "allowed" or "not allowed". Pick one of those, and only write the word.
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
        """
        
        input_messages=[{'role':'system','content':system_prompt}]+messages[-3:]
        
        chatbot_response = get_chatbot_response(self.model_name,messages=input_messages)
        output = self.postprocess(chatbot_response)
        
        return output
    
    def postprocess(self,output):
    
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {"agent":"guard_agent",
                       "guard_decision": output['decision']
                      }
        }
        
        return dict_output