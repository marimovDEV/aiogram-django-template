from aiogram import Router
from .start import router as start_router

# Barcha routerlarni shu yerda jamlaymiz
def setup_handlers() -> Router:
    router = Router()
    router.include_router(start_router)
    return router
