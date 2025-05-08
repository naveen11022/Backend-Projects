from DB import user
from data_validate import signup
from DB import session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter,HTTPException,Response,Depends
from datetime import timedelta, timezone,datetime
import jwt
access_minute = 30

security = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = 'naveen'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()

def create_access_token(data:dict,expire_time:timedelta=None):
    if expire_time:
        expire = datetime.now(timezone.utc) + expire_time
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data ["exp"] = expire.timestamp()

    token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
def signup(Signup:signup):
    user_exists = user(username=Signup.username,password=Signup.password).first()
    if user_exists:
        raise HTTPException({"messages":"Invalid username or password!!!"})
    new_user = user(username=Signup.username,password=Signup.password).save()
    session.add(new_user)
    session.close()
    return Response({"messages":"User created succesfully!!!"})

@router.post("/login", tags=["Authentication"])
def user_login(request: signup):
    user = session.query(user).filter_by(name=request.username, password=request.password).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"username": request.username})
    return {"username": request.username, "message": "Login successful", "token": token}

