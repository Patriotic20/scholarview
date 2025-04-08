from fastapi import APIRouter
from .create import create_router
from .update import update_router
from .delete import delete_router
from .read import read_router


foreign_language_certificates_router = APIRouter(
    tags=["Foreign language certificates"],
    prefix="/foreign_language_certificates"
)


foreign_language_certificates_router.include_router(create_router)
foreign_language_certificates_router.include_router(update_router)
foreign_language_certificates_router.include_router(delete_router)
foreign_language_certificates_router.include_router(read_router)