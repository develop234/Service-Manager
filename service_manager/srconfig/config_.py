from fastapi import FastAPI, status, Depends
from sqlmodel import Session
from create_db import users, engine, signin
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
import json
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from authlib.client.apps import facebook
from starlette.config import Config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


session=Session(bind=engine)

jwt_key = "jwtkey"
api_key = "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"

pwd_cxt = CryptContext(schemes=['bcrypt'],deprecated="auto" )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
app.add_middleware(SessionMiddleware, secret_key="secret-string")

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.testsarp.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/loginf')
async def loginf(request: Request):
    redirect_uri = request.url_for('authg')
    user = await oauth.google.authorize_redirect(request, redirect_uri)
    return user

@app.get('/authf')
async def authf(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return user

@app.get('/loging')
async def loging(request: Request):
    redirect_uri = request.url_for('authg')
    user = await oauth.google.authorize_redirect(request, redirect_uri)
    return user

@app.get('/authg')
async def authg(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return user

@app.post('/signup')
async def signup(user:users):
    HashPass = pwd_cxt.hash(user.password)
    new_user = users(name=user.name,password=HashPass,email=user.email,verified=False)
    token = jwt.encode(user.dict() , jwt_key )
    session.add(new_user)
    session.commit()
    message = Mail(
        from_email='adharun101@sarptest123.com',
        to_emails=new_user.email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='Click the link to verify your account. http://localhost:8000/verifyuser/{}'.format(token))
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        return "Check your email to verify your account"

@app.get('/verify/{token}')
async def verify(token: str):
    payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
    user = session.query(users).filter(payload.get('email')==users.email).first()
    user.verified = True
    session.commit()
    return True

@app.post("/signin")
async def signin(SignIn:signin):
    user = session.query(users).filter(users.email == SignIn.email).first()
    if(user == None):
        return "Account does not exist"
    if user.is_verified == False:
        return "Your account is not verified"
    if pwd_cxt.verify(SignIn.password, user.password):
        token = jwt.encode(user.dict() , jwt_key )
        session.commit()
        return token
    else:
        return "Check your password again"

@app.get("/signin/details")
async def details_of_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
    user = session.query(users).filter(payload.get('email')==users.email).first()
    return user