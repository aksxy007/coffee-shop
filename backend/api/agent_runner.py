from typing import Dict
from agents.gaurd_agent import GaurdAgent
from agents.classification_agent import ClassificationAgent
from agents.agent_protocol import AgentProtocol
from agents.details_agent import DetailsAgent
from agents.order_taking_agent import OrderTakingAgent
from agents.recommendation_agent import RecommendationAgent

import os
import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()

def main():
    gaurdAgent = GaurdAgent()
    classificationAgent=ClassificationAgent()
    recommendationAgent = RecommendationAgent(os.path.join(folder_path,'./recommendation_objects/apriori_recommendations.json'),
                                              os.path.join(folder_path,'./recommendation_objects/popularity_recommendation.csv')
                                              )
    
    
    agent_dict: Dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "order_taking_agent": OrderTakingAgent(recommendationAgent),
        "recommendation_agent": recommendationAgent
    }
    
    messages=[]
    while True:
        # os.system('cls' in os.name=='nt' else 'clear')
        
        print("\n\n Print Messages ..............")
        for message in messages:
            
            print(f"role: {message['role']},content: {message['content']}")
            
        prompt = input("User: ")
        messages.append({"role":"user","content":prompt})
        
        gaurd_agent_response = gaurdAgent.get_response(messages=messages)
        if gaurd_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(gaurd_agent_response)
            continue
        
        classifcation_agent_response =classificationAgent.get_response(messages=messages)
        chosen_agent = classifcation_agent_response["memory"]['classification_decision']
        print("chosen agent: ",chosen_agent)
        
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages=messages)
        
        # print(response)
        messages.append(response)
        
        
if __name__ == "__main__":
    main()

        