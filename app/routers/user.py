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
user_router = APIRouter()


async def authorize_user(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = request.session.get("access_token")
    print("hi")
    if not access_token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    data = verify_access_token(access_token)
    
    if not data:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    if not await check_user(data.get("sub"),db):
        raise HTTPException(status_code=404, detail="User not found")

    return data.get("sub")

@user_router.post("/register")
async def register_user(user_details: Create_User, db:AsyncSession = Depends(get_db)):
    
    data=user_details.model_dump()
    
    #checking if user already exists
    stmt=select(User).where( User.email == data["email"])
    result = await db.execute(stmt)
    result = result.scalar_one_or_none()
    if result:
        raise HTTPException(status_code=409,detail="user already registered")
    
    hashed_password=hash_password(data["password"])
    # adding record in the database
    # record=User(email=data["email"].lower(),first_name=data["first_name"],last_name=data["last_name"],phone_number=data["phone_number"],password=hashed_password.decode("utf-8"))
    # db.add(record)
    stmt = text("""INSERT INTO users (email, first_name, last_name, phone_number, password) values
    (:email, :first_name, :last_name, :phone_number, :password);
    """)
    await db.execute(stmt,{
        "email": data["email"].lower(),
        "first_name": data["first_name"].capitalize(),
        "last_name": data["last_name"].capitalize(),
        "phone_number": data["phone_number"],
        "password": hashed_password
        
    })
    await db.commit()
    
    return JSONResponse(status_code=201, content={'message':'user created successfully'})

@user_router.post("/login")
async def user_login(request:Request, data : Login_User, db:AsyncSession = Depends(get_db)):
    
    login_details=data.model_dump()
    
    stmt=select(User).where( User.email == login_details["email"].lower())
    result = await db.execute(stmt)
    result = result.scalar_one_or_none()
    
    if not result:
        raise HTTPException(status_code=404,detail="user not found")
    
    if verify_password(login_details["password"], result.password):
        access_token=create_access_token({"sub":result.email})
        request.session["access_token"]=access_token
        if access_token:
            
            if result.role == "admin":
                return {"redirect": "/admin-dashboard"}
            else:
                return {"redirect": "/dashboard"}
    else:
        raise HTTPException(status_code=401, detail="Invalid Password")

@user_router.post("/tasks")
async def create_task( request: Request,formData : Task_Struct, user_email:str = Depends(authorize_user), db:AsyncSession = Depends(get_db) ):
    print(request.session)
    if not user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User not autorized")
    task = Task(email=user_email,task_title=formData.task_title,task_description=formData.task_desc)
    db.add(task)
    await db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message':'task created successfully'})

@user_router.get("/tasks")
async def get_tasks(
    user_email: str = Depends(authorize_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(Task.email == user_email)
    )
    tasks = result.scalars().all()

    return [
        {
            "id": task.id,
            "title": task.task_title,
            "description": task.task_description,
        }
        for task in tasks
    ]

@user_router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: Task_Struct,  
    user_email: str = Depends(authorize_user),
    db: AsyncSession = Depends(get_db)
):  
    print(task_id,user_email)
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.email == user_email
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.task_title = task_data.task_title
    task.task_description = task_data.task_desc

    await db.commit()
    await db.refresh(task)

    return JSONResponse(status_code=status.HTTP_200_OK,content={'message':'task updated successfully'})

@user_router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    user_email: str = Depends(authorize_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.email == user_email
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={'message':'Task deleted successfully'})

@user_router.get("/profile")
async def get_tasks(
    user_email: str = Depends(authorize_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user_email)
    )
    data = result.scalar()

    return{
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email
        }

@user_router.put("/profile/update")
async def update_task(
    
    data: Update_User,  
    user_email: str = Depends(authorize_user),
    db: AsyncSession = Depends(get_db)
):  
    await db.execute(
        update(User).where(
            User.email == user_email
        ).values(first_name=data.first_name,last_name=data.last_name)
    )
    
    await db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,content={'message':'profile updated successfully'})

@user_router.delete("/logout")
def logout_user(request: Request):
    request.session["access_token"] = None
    
    if request.session.get("access_token"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return {"redirect_url":"/login"}
      
# @user_router.put("/edit")
# async def update_user(email:EmailStr,new_details:Update_User, db:AsyncSession = Depends(get_db)):
    
#     data=new_details.model_dump(exclude_unset=True)
#     email=email.lower()
#     #checking if user already exists
#     stmt=select(User).where( User.email == email)
#     result = await db.execute(stmt)
#     result = result.scalar_one_or_none()
#     if not result:
#         return HTTPException(status_code=404,detail="user not found")
    
#     #updating detail after confirming their existence
#     if "first_name" in data:
#         stmt=update(User).where(User.email == email).values(first_name=data["first_name"].capitalize())
#         await db.execute(stmt)
#     if "last_name" in data:
#         stmt=update(User).where(User.email == email).values(last_name=data["last_name"].capitalize())
#         await db.execute(stmt)
#     if "password" in data:
#         stmt=update(User).where(User.email == email).values(password=data["password"])
#         await db.execute(stmt)
    
#     await db.commit()
#     return JSONResponse(status_code=200,content={'message':'details updated successfully'})

# @user_router.delete("/delete")
# async def delete_user(email:EmailStr , db:AsyncSession = Depends(get_db)):
#     email=email.lower()
#     #checking if user already exists
#     stmt=select(User).where( User.email == email)
#     result = await db.execute(stmt)
#     result = result.scalar_one_or_none()
#     if not result:
#         return HTTPException(status_code=404,detail="user not found")
    
#     # stmt=delete(User).where(User.email == email)
#     stmt=text("""DELETE FROM users where email = :email
#               """)
#     await db.execute(stmt,{"email":email})
#     await db.commit()
#     return JSONResponse(status_code=200,content={"message":"user_details deleted successfully"})

# @user_router.get("/view")
# async def get_users(db:AsyncSession = Depends(get_db)):
    
#     data = await db.execute(select(User))
#     data = data.scalars().all() 
#     return [{
#         "email": user.email,
#         "first_name": user.first_name.capitalize(),
#         "last_name": user.last_name.capitalize()
#     } for user in data]


    