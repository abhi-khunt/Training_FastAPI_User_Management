from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings   


DATABASE_URL = settings.database_url


#Create Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Shows SQL queries in terminal (good for debugging)
)

class Base(DeclarativeBase):
    pass

#Create Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

#Dependency for routes
async def get_db():
  
    async with AsyncSessionLocal() as session:
    
        yield session
       