from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.users import router as users_router
from src.api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(users_router, prefix="/v1")
    app.include_router(auth_router, prefix="/v1")
    return app
