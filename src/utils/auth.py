from jose import JWTError , jwt , ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta , datetime
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from src.models.user import User
from src.core.base import get_db 
from fastapi import Depends , HTTPException , status
import asyncio




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")




async def hash_password(password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash , password)


async def verify_password(plain_password: str , hashed_password: str ) -> bool:
    return await asyncio.to_thread(pwd_context.verify, plain_password , hashed_password)


async def create_access_token(data: dict , expires_delta: timedelta ) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})

    return await asyncio.to_thread(jwt.encode , to_encode , settings.SECRET_KEY , algorithm = settings.ALGORITHM)



async def create_refresh_token(data: dict , expire_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expire_delta
    to_encode.update({"exp": expire})

    return await asyncio.to_thread(jwt.encode , to_encode , settings.REFRESH_SECRET_KEY , algorithm = settings.ALGORITHM)


async def verify_token(token: str , secret_key: str):
    try:
        payload = await asyncio.to_thread(jwt.decode , token , secret_key , algorithms = [settings.ALGORITHM])
        return payload
    
    except ExpiredSignatureError:
        unverified_payload = jwt.get_unverified_claims(token)
        unverified_payload.setdefault("is_expired", True)
        return unverified_payload
    except JWTError:
        return None


async def get_user(db: AsyncSession , username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession , username: str , password: str):
    user = await get_user(db , username)
    if not user or not await verify_password(password , user.password):
        return None
    return user

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    payload = await verify_token(token=token , secret_key=settings.SECRET_KEY)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    username = payload.get("seb")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token paload"
        )
    
    user = await get_user(db , username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user