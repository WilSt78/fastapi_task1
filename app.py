from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers.base import router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/v1", tags=["Base APIs"])
    return app
