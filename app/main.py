from app.application import create_app
from app.database.config import get_production_db_url

app = create_app(get_production_db_url())
