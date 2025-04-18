from fastapi import APIRouter
from .achievements import achievements_router
from .foreign_language_certificates import foreign_language_certificates_router
from .scientific_research_work import scientific_research_work_router

user_router = APIRouter()


user_router.include_router(achievements_router)
user_router.include_router(foreign_language_certificates_router)
user_router.include_router(scientific_research_work_router)
