from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from jwt import PyJWTError
import jwt
from Articles import User

security = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = 'naveen'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()


class user(BaseModel):
    username : str
    password:  str

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(
        minutes= ACCESS_TOKEN_EXPIRE_MINUTES))
    data["exp"] = expire.timestamp()
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(security)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = username.get("exp")
        if exp_time:
            exp_time = datetime.fromtimestamp(exp_time, timezone.utc)
            if exp_time < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token has expired")

        user = User.objects.filter(username=username["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/signup", tags=["Authentication"])
def user_signup(request: user):
    user = User.objects.filter(username=request.username, password=request.password).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    User(username=request.username, password=request.password).save()
    return {"username": request.username, "details": "User created successfully"}


@router.post("/login", tags=["Authentication"])
def user_login(request: user):
    user = User.objects.filter(username=request.username, password=request.password).first()
    if user:
        token = create_access_token(data={"username": request.username})
        return {"username": request.username, "message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")
