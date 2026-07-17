from fastapi import FastAPI

from app.api.api import router
from app.api.exception_handlers import create_handlers
from app.persistence.tables import engine, metadata

app = FastAPI()
app.include_router(router)


def initialize():
    metadata.create_all(engine, checkfirst=True)


initialize()
create_handlers(app)
