import bcrypt
from datetime import UTC, datetime, timedelta
import jwt
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User


def hash_password(password:str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

def verify_password(password:str ,hashed_password:str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"),hashed_password.encode("utf-8"))

def create_access_token(data: dict , expires_delta: timedelta | None = None) -> str :
    to_encode = data.copy()
    if expires_delta:
         expire =datetime.now(UTC) + expires_delta  
    else:
        expire = datetime.now(UTC) + timedelta(minutes= settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire} )
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )
    
    return encoded_jwt

def verify_access_token(token: str):
    try: 
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require":["exp","sub"]}
        ) 
    except jwt.InvalidTokenError:
        return None
    else:
        return payload

async def check_user(email:str,db:AsyncSession) -> bool:
    
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user_data = result.scalar_one()
    if user_data.email :
        return True
    else:
        return False