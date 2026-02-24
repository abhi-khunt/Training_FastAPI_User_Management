from pydantic import BaseModel, EmailStr, Field
from typing import Annotated,Optional

class Task_Struct(BaseModel):
    task_title:Annotated[str,Field(...,description="Task_title", max_length=255)]
    task_desc: Annotated[str, Field(...,description="Task Description", max_length=500)]