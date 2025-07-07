from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from models import Base, User, Task
from database import engine, SessionLocal
from schemas import UserCreate, TaskCreate, UserOut, TaskUpdate, TaskOut
from sqlalchemy import asc, desc


#Create tables and models
Base.metadata.create_all(bind=engine)

app = FastAPI()


#Get Session
def get_db():
    try:
        db = SessionLocal()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    try:
        yield db
    finally:
        db.close()


#POST USERS
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET ALL USERS
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# POST TASKS
@app.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        done = task.done
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# GET USER BY ID
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# PUT TASK BY ID
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.done is not None:
        task.done = task_update.done

    db.commit()
    db.refresh(task)
    return task


# DELETE TASK BY ID
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return


#GET TASK BY FILTERS AND ORDERING
@app.get("/tasks/")
def read_tasks(
    user_id: int = None,
    title: str = None,
    done: bool = None,
    sort_by: str = "id",  # default sort
    order: str = "asc",   # default order
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    # Apply filters
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)
    if title is not None:
        query = query.filter(Task.title == title)
    if done is not None:
        query = query.filter(Task.done == done)

    # Apply sorting
    sort_column = getattr(Task, sort_by, None)
    if sort_column is None:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")

    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    results = query.all()
    if not results:
        return {"message": "No tasks found"}
    return results


# GET TASK BY ID
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task