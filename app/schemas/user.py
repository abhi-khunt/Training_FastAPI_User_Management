from pydantic import BaseModel, EmailStr, Field
from typing import Annotated,Optional

class User(BaseModel):
    email: Annotated[EmailStr,Field(...,description="E-mail field")] 
    
class Login_User(User):
    password: Annotated[str, Field(...,description="Password field",min_length=8)]   
    
class Create_User(Login_User):
    first_name: Annotated[str,Field(...,description="First Name field",min_length=1,max_length=25)]
    last_name: Annotated[str,Field(...,description="Last Name field",min_length=1,max_length=25)]
    phone_number: Annotated[str,Field(...,description="Phone number field", min_length=10,max_length=10)]
    
    
class Update_User(BaseModel):
    first_name: Annotated[Optional[str],Field(None,description="First Name field",min_length=1,max_length=25)]
    last_name: Annotated[Optional[str],Field(None,description="Last Name field",min_length=1,max_length=25)]
    
    
