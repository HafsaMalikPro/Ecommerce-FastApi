from passlib.context import CryptContext
from dotenv import dotenv_values
import jwt
from fastapi import (FastAPI, Depends, HTTPException, status)
from models import (User, Business, Product, user_pydantic, user_pydanticIn, 
                    product_pydantic,product_pydanticIn, business_pydantic, 
                    business_pydanticIn)



config_credentials = dict(dotenv_values(".env"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    return pwd_context.hash(password)



async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials['SECRET'], algorithms = ['HS256'])
        user = await User.get(id = payload.get('id'))
    except:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user