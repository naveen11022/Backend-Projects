from fastapi import APIRouter,HTTPException,Response,Depends
from fastapi.security import OAuth2PasswordBearer
from Db import user,session
from data_validate import signup
from datetime import datetime, timedelta,timezone
import jwt
ACCESS_MINUTES = 30
SECURITY = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = 'HS256'
secret_key = 'vkjbiiuvh3039i-20r[kf=r0o=1o=fk3[ompoj]]'


router = APIRouter()

def create_access_token(data:dict,expire_time:timedelta=None):
    if expire_time:
        expire = datetime.now(timezone.utc) + expire_time

    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_MINUTES)
    data["exp"] = expire
    token = jwt.encode(data,secret_key,ALGORITHM)
    return token

     
def get_current_user(token: str = Depends(SECURITY)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        exp_time = payload.get("exp")
        if exp_time:
            exp_time = datetime.fromtimestamp(exp_time, timezone.utc)
            if exp_time < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token has expired")

        user = session.query(user).filter_by(name=payload["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    

@router.post("/signup")
def signup(signup:signup):
    user_exists = session.query(signup.username,signup.password).filter(name=signup.name,password=signup.password).first()
    if user_exists:
        raise HTTPException({"messages":"Invalid username or password"},status_code=401)
    new_user = user(name=signup.username,password=signup.password)
    session.add(new_user)
    session.close()
    return Response({"messages":"User created Successfully!!!"})

@router.post("/login")
def login(login:signup):
        user_exists = session.query(signup.username,signup.password).filter(name=signup.name,password=signup.password).first()
        if not user_exists:
             raise HTTPException({"messages":"User not found!!!"},status_code=401)
        
        token = create_access_token(data={"username": login.username})
        return {"username": login.username, "message": "Login successful", "token": token}

