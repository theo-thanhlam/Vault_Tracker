import bcrypt
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from ..models import UserModel, VerificationModel
import jwt
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .  import db
from dotenv import load_dotenv
import re

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
        
        cls._session.add(VerificationModel(token=token))
        cls._session.commit()
        return token
    
    @classmethod
    def create_login_token(cls,id:UUID):
        payload = {
            "id":str(id),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        }
        token = jwt.encode(payload, key=cls._LOGIN_SECRET,algorithm="HS256")
        # cls._session.add(VerificationModel(token=token))
        # cls._session.commit()
        return token
    
    @classmethod
    def verify_signup_token(cls, token:str) -> dict:
        payload = jwt.decode(token,key=cls._SIGNUP_SECRET,algorithms="HS256")
        return payload
    
    @classmethod
    def verify_login_token(cls, token:str):
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
    
    verify_endpoint = f"{_API_URL}/verify-email"
    
    
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
        