from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


#Create Users Table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    
    tasks = relationship("Task", back_populates="user")
    
#Create Tasks table 
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey("users.id"))
    done = Column(Boolean, default=False) 
    
    user = relationship("User", back_populates="tasks")