from fastapi import FastAPI
from endpoints import chat,auth
from db.mongodb_connection import connect_to_mongo,close_mongo_connection
from db.utils import check_collection_exists
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
global db;

origins=[]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include the chat router
app.include_router(chat.router, prefix="/chat")
app.include_router(auth.router,prefix="/auth")