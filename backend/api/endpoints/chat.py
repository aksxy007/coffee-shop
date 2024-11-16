from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent_controller import AgentController
from sessions.session_manager import get_current_user
from models.Chat import Chat
from models.Query import ChatQuery
from db.utils import save_chat,get_chat_history
from datetime import datetime
import logging

router = APIRouter()


@router.post('/get-response')
async def get_agent_response(query: ChatQuery,current_user_id: str = Depends(get_current_user)):
# async def get_agent_response(query: ChatQuery):
    try:
        # Initialize the agent controller
        print(current_user_id)
        agentController = AgentController()
        messages = await get_chat_history(str(current_user_id))
        # Get the response from the agent controller
        user_chat = Chat(user_id=str(current_user_id), role="user", content=query.query)
        messages.append(user_chat.dict(exclude_unset=True))
        response = agentController.get_response(messages)
        print(response)
        try:
           res= await save_chat(user_chat)
           logging.info(res)
        except Exception as e:
           logging.error(f"Failed to save the chat: {e}") 
           
        try:
            print(type(response))
            if type(response)==str:
                response_chat= Chat(user_id=str(current_user_id),role='assistant',content=response)
                response  = {"role":"assitant","content":response}
            else:
                response_chat= Chat(user_id=str(current_user_id),role=response['role'],content=response['content'])
            res= await save_chat(response_chat)
            logging.info(res)
        except Exception as e:
           logging.error("Failed to save the chat") 
        
        return JSONResponse(content={"message": response}, status_code=200)
    
    except Exception as e:
        # Return an error response using JSONResponse
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500
        )
    
    
    