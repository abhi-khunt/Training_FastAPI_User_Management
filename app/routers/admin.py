from fastapi import APIRouter,Depends,HTTPException,Request, status
from fastapi.responses import JSONResponse,RedirectResponse, Response
from fastapi.requests import Request
from datetime import timedelta
from pydantic import EmailStr
from sqlalchemy import select, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import Create_User, Update_User, Login_User
from app.schemas.task import Task_Struct
from app.db.database import get_db
from app.models.user import User
from app.models.task import Task
from app.core.auth import hash_password, verify_password, create_access_token, verify_access_token, check_user

async def authorize_user(request:Request, db:AsyncSession=Depends(get_db)) -> str:
    access_token = request.session.get("access_token")
    if  not access_token :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
    data=verify_access_token(access_token)
    
    if not data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Token expired login again")
    
    result = await db.execute(select(User).where(User.email==data.get("sub")))
    user_data = result.scalar_one()
    if not (user_data.email and user_data.role=="admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized")
    return user_data.role
    
admin_router=APIRouter()

@admin_router.get("/users")
async def get_users(role:str = Depends(authorize_user), db:AsyncSession=Depends(get_db)):
    
    stmt = select(User).where(User.role != role)
    result= await db.execute(stmt)
    users_data = result.scalars().all()
    
    return[
        {
           "id": user.id,
           "first_name": user.first_name,
           "last_name": user.last_name,
           "email":user.email,
           "role": user.role
           
        }for user in users_data
    ]

@admin_router.put("/users/{user_id}/promote")
async def promote_user(user_id:int,role:str = Depends(authorize_user),db:AsyncSession = Depends(get_db)):
    try:
        print(user_id)
        stmt=update(User).where(User.id==user_id).values(role="sub-admin")
        await db.execute(stmt)
        await db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={'message':'promoted successfully'})
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@admin_router.delete("/users/{user_id}/delete")
async def delete_user(user_id:int,role:str = Depends(authorize_user),db:AsyncSession = Depends(get_db)):
    try:
        print(user_id)
        stmt=delete(User).where(User.id==user_id)
        await db.execute(stmt)
        await db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={'message':'promoted successfully'})
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)