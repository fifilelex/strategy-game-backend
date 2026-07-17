from fastapi import FastAPI

from app.api.api import router
from app.api.exception_handlers import create_handlers
from app.persistence.init_db import initialize_db
from app.persistence.tables import engine

app = FastAPI()
app.include_router(router)


initialize_db(engine)
create_handlers(app)
