from sqlalchemy import String,DateTime ,column, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    email:Mapped[str] = mapped_column(String(255),nullable=False)
    task_title:Mapped[str] = mapped_column(String(255), nullable=False)
    task_description:Mapped[str] = mapped_column(String(500),nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())