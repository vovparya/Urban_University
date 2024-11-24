from fastapi import APIRouter

from app.models import User
from app.schemas import CreateUser, UpdateUser

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
async def all_users():
    pass


@router.get("/{user_id}")
async def user_by_id(user_id: int):
    pass


@router.post("/create")
async def create_user():
    pass


@router.put("/update")
async def update_user():
    pass


@router.delete("/delete")
async def delete_user():
    pass
