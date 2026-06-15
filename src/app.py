import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routers.auth import router as auth_router
from src.api.routers.category import router as category_router
from src.api.routers.comment import router as comment_router
from src.api.routers.location import router as location_router
from src.api.routers.post import router as post_router
from src.api.routers.users import router as users_router
from src.infrastructure.database import database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield
    await database.dispose()


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,  
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(users_router, tags=["Base APIs"])
    app.include_router(auth_router, prefix="/auth", tags=["Base APIs"])
    app.include_router(location_router)
    app.include_router(category_router)
    app.include_router(post_router)
    app.include_router(comment_router)

    return app