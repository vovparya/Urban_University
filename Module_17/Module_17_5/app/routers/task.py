from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask

router = APIRouter(
    prefix="/task",
    tags=["tasks"]
)


@router.get("/", response_model=List[CreateTask])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks


@router.get("/{task_id}", response_model=CreateTask)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.post("/create/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_task(
        user_id: int,
        task_data: CreateTask,
        db: Annotated[Session, Depends(get_db)]
):
    # Проверяем, существует ли пользователь с данным user_id
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    slug = slugify(task_data.title)
    new_task = Task(
        title=task_data.title,
        content=task_data.content,
        priority=task_data.priority,
        user_id=user_id,
        slug=slug
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{task_id}")
async def update_task(
        task_id: int,
        task_data: UpdateTask,
        db: Annotated[Session, Depends(get_db)]
):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task:
        db.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(
                title=task_data.title if task_data.title is not None else task.title,
                content=task_data.content if task_data.content is not None else task.content,
                priority=task_data.priority if task_data.priority is not None else task.priority,
                completed=task_data.completed if task_data.completed is not None else task.completed,
            )
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")
