from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from db.session_utils import delete_session
from sessions.session_manager import get_current_user
from sessions.jwt_utils import create_access_token
from sessions.utils import hash_password, verify_password
from db.auth_utils import get_user_by_email,register_user
from models.Register import UserRegister
from models.Login import UserLogin
import logging

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@router.post("/register")
async def register(user: UserRegister):
    try:
        # Check if the user already exists
        print("user", user)
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash the password
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        print(user.password)

        # Save the user to the database
        user = await register_user(user)
        
        return {"user": user}

    except Exception as e:
        # Log the error and raise a generic error message
        logging.error(f"Error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user",
        )

@router.post("/login")
async def login(payload:UserLogin):
    
    user = payload
    db_user = await get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Create and return JWT token
    access_token =await create_access_token(data={"sub": str(db_user["_id"])})
    user = user.dict()
    user["id"] = str(db_user["_id"])
    user['username'] = db_user['username']

    return {"user":user, "access_token": access_token}

@router.get("/profile")
async def get_profile(current_user_id: str = Depends(get_current_user)):
    return {"user": current_user_id}

@router.post("/logout")
async def logout(current_user_id: str = Depends(get_current_user)):
    token = oauth2_scheme(tokenUrl="login")  # Extract current token
    await delete_session(token)
    return {"message": "Logged out successfully"}
