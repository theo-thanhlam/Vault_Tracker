import bcrypt
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from ..models import UserModel, TokenModel, TransactionModel,TokenTypeEnum
import jwt
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .  import db
from dotenv import load_dotenv
import re
from functools import wraps
from strawberry.types import Info
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
load_dotenv()

class AuthHandler:
    _salt = bcrypt.gensalt(rounds=12)
    
    @classmethod
    def hash_password(cls,password:str):
        encoded = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password=encoded, salt=cls._salt)
        return hashed_password.decode("utf-8")
    
    @staticmethod
    def verify_password(password:str, hashed_password:str):
        encoded_password = password.encode('utf-8')
        encoded_hashed_password=hashed_password.encode("utf-8")
        
        check = bcrypt.checkpw(password=encoded_password, hashed_password=encoded_hashed_password)
        return check
    
    @staticmethod
    def check_valid_email(email:str):
        _email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(_email_regex, email)

    @staticmethod
    def check_valid_password(password:str):
        _strong_password_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return re.fullmatch(_strong_password_regex, password) 
    
    @staticmethod
    def verify_email(token:str):
        try:
            # Check if register token exists in database
            session = db.get_session()
            token_existed = session.get(TokenModel, token)
            if not token_existed:
                return {"message":"Invalid Token", "status_code": 401}
            
            #Check valid token
            decoded_token=JWTHandler.verify_signup_token(token=token)
            if not decoded_token:
                return {"message":"Invalid token", "status_code":401}
            
            user_id = decoded_token.get("id")
            user = session.query(UserModel).filter(UserModel.id == user_id).first()

            if not user:
                return {"message":"User does not exist", "status_code":400}

            if user.email_verified:
                return {"message": "User already verified", "status_code":403}

            user.email_verified = True
            session.commit()

            return {"message": "Email verified successfully", "status_code":200}
        except Exception as e:
            pass
        
    @staticmethod
    async def verify_google_token(token:str):
        try:
            GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            return id_info
        except ValueError as e:
            return None
    
    
        

class DatabaseHandler:
    
    @staticmethod
    def create_new_user(session:Session, user_doc:UserModel):
        try:
            session.add(user_doc)
            session.commit()
            session.refresh(user_doc)
        except Exception as e:
            print("CREATE USER ERROR")
            return
    
    @staticmethod    
    def get_user_by_email(session:Session, email:str):
        return session.query(UserModel).filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_id(session:Session, id:UUID):
        return session.get(UserModel,id)

    @staticmethod
    def create_new_transaction(session:Session, transaction_doc:TransactionModel):
        try:
            session.add(transaction_doc)
            session.commit()
            session.refresh(transaction_doc)
        except Exception as e:
            print("CREATE EXPENSE ERROR")
            print(e)
            raise 
    
    @staticmethod
    def get_transaction_by_id(session:Session, id:str):
        return session.query(TransactionModel).filter_by(id=id).first()
    
    @staticmethod
    def get_all_transactions_by_user_id(session:Session, user_id:UUID):
        return session.query(TransactionModel).filter_by(user_id=user_id).all()
        
    
    
class JWTHandler:
    _SIGNUP_SECRET = os.getenv("SIGNUP_SECRET")
    _LOGIN_SECRET = os.getenv("LOGIN_SECRET")
    _session:Session = db.get_session()
    
    
    @classmethod
    def create_signup_token(cls,id:UUID):
        payload = {
            "id":str(id),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, key=cls._SIGNUP_SECRET, algorithm="HS256")
        
        cls._session.add(TokenModel(token=token, type=TokenTypeEnum.REGISTER))
        cls._session.commit()
        return token
    
    @classmethod
    def create_login_token(cls,id:UUID):
        payload = {
            "id":str(id),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        }
        token = jwt.encode(payload, key=cls._LOGIN_SECRET,algorithm="HS256")
        cls._session.add(TokenModel(token=token, type=TokenTypeEnum.LOGIN))
        cls._session.commit()
        return token
    
    @classmethod
    def verify_signup_token(cls, token:str) -> dict | None:
        if token:
            payload = jwt.decode(token,key=cls._SIGNUP_SECRET,algorithms="HS256")
            return payload
    
    @classmethod
    def verify_login_token(cls, token:str) -> dict | None:
        if token:
            payload = jwt.decode(token,key=cls._LOGIN_SECRET,algorithms="HS256")
            return payload
    
class EmailHandler:
    smtp_config = {
        "host":"smtp.gmail.com",
        "port":587,
        "username":os.getenv("SMTP_USERNAME"),
        "password":os.getenv("SMTP_APP_PASSWORD"),
        "from_email":os.getenv("SMTP_USERNAME")
    }
    _API_URL = os.getenv("API_URL")
    
    verify_endpoint = f"{_API_URL}/auth/verify-email"
    
    
    @classmethod
    def send_verification_email(cls, token:str, user_email:str):
        verify_url = f"{cls.verify_endpoint}?token={token}"
        email_body = f"Click the link below to verify your email:\n\n{verify_url}"
        email_subject = "Verify your email address"
        msg = MIMEMultipart()
        msg["From"] = cls.smtp_config["from_email"]
        msg["To"] = user_email
        msg["Subject"] = email_subject

        msg.attach(MIMEText(email_body, "plain"))

        with smtplib.SMTP(cls.smtp_config["host"], cls.smtp_config["port"]) as server:
            server.starttls()
            server.login(cls.smtp_config["username"], cls.smtp_config["password"])
            server.send_message(msg)


def login_required(resolver):
    
    @wraps(resolver)
    def wrapper(*args, info: Info, **kwargs):
        user = info.context.get("user")
        if not user:
            raise HTTPException(detail="Please login before proceed",status_code=401)
        if not user.email_verified:
            raise HTTPException(detail="Your account is not verified",status_code=401)
        return resolver(*args, info=info, **kwargs)
    return wrapper