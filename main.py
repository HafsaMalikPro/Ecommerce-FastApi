from fastapi import (FastAPI, BackgroundTasks, UploadFile, 
                    File, Form, Depends, HTTPException, status, Request)
from tortoise.contrib.fastapi import register_tortoise
from tortoise import models
from models import *
from authentication import *
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from starlette.responses import JSONResponse

#signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from emails import *

# HTMLResponse
from fastapi.responses import HTMLResponse


# templates
from fastapi.templating import Jinja2Templates

# Initialize Jinja2Templates with the directory containing your HTML templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')




@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    if created:
        business_obj = await Business.create(
            business_name=instance.username, owner=instance)
        
        await business_pydantic.from_tortoise_orm(business_obj)
        #send the email to the user
        await send_email([instance.email], instance)



@app.post("/registration")
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status": "ok",
        "data": f"Hello {new_user.username}, thanks for choosing our services.Please check your email inbox and click on the link to confirm your registration."
    }


@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
   user = await verify_token(token)
   if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html", 
                                {"request": request, "username": user.username} 
                             )
   raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]}, 
    generate_schemas=True,
    add_exception_handlers=True
) 