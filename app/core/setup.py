from alembic.config import Config, command
from fastapi import APIRouter, FastAPI

from fastapi.middleware.cors import CORSMiddleware


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def create_application(router: APIRouter):
    run_migrations()
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app
