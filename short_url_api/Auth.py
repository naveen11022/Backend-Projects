from DB import user,session
from fastapi import APIRouter,HTTPException,Depends,Response
from fastapi.security import OAuth2PasswordBearer
from data_validate import user,shorturl
from datetime import timedelta, timezone,datetime
import jwt
SECURITY = OAuth2PasswordBearer(tokenUrl='/login')
ACCESS_MINUTES = 30
ALGORITHM = 'HS256'
SECRET_KEY = 'knvkjnrkjbndkhfkbjn'

router = APIRouter()

def create_access_token(data:dict,expire:timedelta=None):
    if expire:
        expire = datetime.now(timezone.utc) + expire
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_MINUTES)

        data ["exp"] = expire.timestamp()

        token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
        return token
    
def get_current_user(token:str=Depends(SECURITY)):
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
def signup(User:user):
    user_exists = session.query(user).filter(username=User.username,password=User.password)
    if user_exists:
        raise HTTPException({"messages":"Invalid username or password"},status_code=401)
    user(username = User.username,password = User.password)
    session.add(user)
    session.close()
    return Response({"messages":"User created successfully"})

@router.post("/login")
def login(User:user):
    user_exists = session.query(user).filter(username=User.username,password=User.password)
    if not user_exists:
        raise HTTPException({"messages":"Invalid username or password"},status_code=401)
    token = create_access_token(data={"username":User.username})
    return token
