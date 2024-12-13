from fastapi import (BackgroundTasks, UploadFile, 
                    File, Form, Depends, HTTPException, status)

from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
from dotenv import dotenv_values
import jwt
from models import User

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
  MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Correct field name
    MAIL_SSL_TLS=False,  # Correct field name
    USE_CREDENTIALS=True
    
    
    # MAIL_USERNAME = config_credentials["EMAIL"],
    # MAIL_PASSWORD = config_credentials["PASS"],
    # MAIL_FROM = config_credentials["EMAIL"],
    # MAIL_PORT = 587,
    # MAIL_SERVER = "smtp.gmail.com",
    # MAIL_TLS = True,
    # MAIL_SSL = False,
    # USE_CREDENTIALS = True
)



class EmailSchema(BaseModel):
    email: List[EmailStr]
    
    

async def send_email(email : List, instance: User):

    
    token_data = {
        "id" : instance.id,
        "username" : instance.username
    }

    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")
    
    template = f"""
        <!DOCTYPE html>
    <html>
        <head>
            <title>Email Verification</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px; text-align: center; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); " >

            <h1>Hello {instance.username},</h1>
            <p>Please verify your email address by clicking the link below:</p>
            <a href="http://localhost:8000/verification/?token={token}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px;" >Verify Email</a>

            <p>Thank you for choosing our platform.</p>
            
            
            
            <p>If you are having trouble clicking the link, copy and paste the URL below into your web browser:</p>
            <a href="http://localhost:8000/verification/?token={token}">http://localhost:8000/verification/?token={token}</a>
            
            <p>For security purposes, please do not share this email address with anyone else.</p>
            <p>This email is confidential and intended for the sole use of the recipient.</p>
            <p>If you have any questions or concerns, please contact us at <a href="mailto:stylinalivlogs@gmail.com">hafsamalik2585@gmail.com</a></p>
            
            
            <p>Please kindly ignore this email if you did not register on our platform.</p>
            <p>This email is automatically generated. Please do not reply.</p>
            <p>&copy; 2024 All rights reserved.</p>

            <p>Best regards,</p>
            <p>"Hafsa Malik"</p>
            
        </div>
        </body>
        </html>
    """
    
    message = MessageSchema(
        subject="Ecommerce Account Verification Mail",
        recipients=email,  
        body=template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message) 