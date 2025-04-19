from fastapi import APIRouter

from app.api.routes import (
    items,
    login,
    private,
    users,
    utils,
    ai_automation_productivity,
    ai_bussiness_data_analysis,
    ai_chatbot_virtual_assistants,
    ai_developer_coding,
    ai_text_processing_nlp,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(ai_automation_productivity.router)
api_router.include_router(ai_bussiness_data_analysis.router)
api_router.include_router(ai_chatbot_virtual_assistants.router)
api_router.include_router(ai_developer_coding.router)
api_router.include_router(ai_text_processing_nlp.router)
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
