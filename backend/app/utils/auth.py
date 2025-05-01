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


load_dotenv()




def hash_password(password:str):
    _salt = bcrypt.gensalt(rounds=12)
    encoded = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password=encoded, salt=_salt)
    return hashed_password

def verify_password(password:str, hashed_password):
    encoded = password.encode('utf-8')
    check = bcrypt.checkpw(password=encoded, hashed_password=hashed_password)
    return check

def create_new_user(session:Session, user_doc:UserModel):
    try:
        session.add(user_doc)
        session.commit()
        session.refresh(user_doc)
    except Exception as e:
        print("CREATE USER ERROR")
        return
    
def get_user_by_email(session:Session, email:str):
    return session.query(UserModel).filter_by(email=email).first()

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
        cls._session.add(token)
        cls._session.commit()
        return token
    
    @classmethod
    def verify_signup_token(cls, token:str):
        pass
    @classmethod
    def verify_login_token(cls, token:str):
        pass
    
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
        