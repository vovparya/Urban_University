from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List

from sqlalchemy import insert, select, update, delete
from slugify import slugify

from app.backend.db_depends import get_db
from app.models.user import User
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser, CreateTask

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.get("/", response_model=List[CreateUser])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


@router.get("/{user_id}", response_model=CreateUser)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.get("/{user_id}/tasks", response_model=List[CreateTask])
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")
    tasks = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return tasks


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user_data.username)
    new_user = User(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age,
        slug=slug
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                age=user_data.age
            )
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        # Удаляем задачи, связанные с пользователем
        db.execute(delete(Task).where(Task.user_id == user_id))
        # Удаляем самого пользователя
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User and related tasks deletion is successful!"}
    else:
        raise HTTPException(status_code=404, detail="User was not found")
