from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"],
    
)


fake_users_db = {
    "email":"email@gmail.com",
    "password":"johndoe1234123"
}


@router.get("/")
async def get_users():
    return fake_users_db