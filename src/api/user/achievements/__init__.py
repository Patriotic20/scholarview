from fastapi import APIRouter
from .create import create_router
from .update import update_router
from .delete import delete_router
from .read import read_router


achievements_router = APIRouter(
    tags=["Achievement"],
    prefix="/achievement"
)


achievements_router.include_router(create_router)
achievements_router.include_router(update_router)
achievements_router.include_router(delete_router)
achievements_router.include_router(read_router)