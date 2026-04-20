from fastapi import APIRouter
from app.modules.grades.router import router as grades_router
from app.modules.nationalities.router import router as nationalities_router
from app.modules.registrations.router import router as registrations_router
from app.modules.school_years.router import router as school_years_router
from app.modules.students.router import router as students_router
from app.modules.subjects.router import router as subjects_router

api_router = APIRouter()

for router in (
    grades_router,
    subjects_router,
    school_years_router,
    students_router,
    registrations_router,
    nationalities_router,
):
    api_router.include_router(router)