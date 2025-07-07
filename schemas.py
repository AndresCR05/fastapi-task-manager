from pydantic import BaseModel, EmailStr
from typing import List, Optional


# CLASS FOR CREATE USER
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# CLASS FOR CREATE TASK 
class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int
    done: Optional[bool] = False 
    
# CLASS FOR GET TASK    
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool

    model_config = {
        "from_attributes": True
    }

# CLASS FOR GET USER
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    tasks: List[TaskOut] = [] 

    model_config = {
        "from_attributes": True
    }
    
# CLASS FOR UPDATE TASK
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }