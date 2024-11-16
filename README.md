# Coffee Shop App


### This is a coffee shop react native app.This is AI powered chatbot to enhance the customer experience. Leveraging the power of LLMs (Large Langauge Models) ,agents,NLP(Natural Language Processing), the chatbot can assits in listing out details of specific products , about the shop itself, also in taking orders and giving personalised product recommendations on the go to the customers-- all in a single app.


# Project Overview

### The goal of this project is to create a smart, agent-based chatbot that can:

-Handle real-time customer interactions with the chatbot including orders.
-Answer questions about menu items, including ingredients and allergens through a Retreival augmented Generation (RAG) system.
-Provide personalized product recommendations through a market basket analysis recommendation engine.
-Guide customers through a seamless order process, ensuring accurate and structured order details.
-Block irrelevant or harmful queries using a Guard Agent for safe and relevant interactions.

# Key Agents in the System:
1.Guard Agent: This agent acts as the first line of defense. It monitors all incoming user queries and ensures that only relevant and safe messages are processed by the other agents. It blocks inappropriate, harmful, or irrelevant queries, protecting the system and ensuring smooth conversations with users.

2.Order Taking Agent: This agent is responsible for guiding customers through the order placement process. It uses chain-of-thought prompt engineering to simulate human-like reasoning, ensuring the order is accurately structured and all customer preferences are captured. It ensures that the chatbot gathers all necessary order details in a logical, step-by-step process, enhancing the reliability of the final order.

3.Details Agent (RAG System): Powered by a Retrieval-Augmented Generation (RAG) system, the Details Agent answers specific customer questions about the coffee shop, including menu details, ingredients, allergens, and other frequently asked questions. It retrieves relevant data stored in the vector database and combines it with language generation capabilities to provide clear and precise responses.

4.Recommendation Agent: This agent handles personalized product recommendations by working with the market basket recommendation engine. Triggered by the Order Taking Agent, it analyzes the user's current order or preferences and suggests complementary items. This agent aims to boost upselling opportunities or help users discover new products they might like.

5.Classification Agent: This is the decision-making agent. It classifies incoming user queries and determines which agent is best suited to handle the task. By categorizing user intents, it ensures that queries are routed efficiently, whether the user is asking for recommendations, placing an order, or inquiring about specific menu details.


# ChatBot Architecture:

![ChatBot Architecture](/Coffee Shop Agent Arch.png 'ChatBot Architecture')