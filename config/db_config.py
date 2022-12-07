from dotenv import load_dotenv
from sqlalchemy import create_engine

import os
import psycopg2 as pg




_ = load_dotenv()

CONN = pg.connect(
    database = os.environ.get("DB_DATABASE"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASSWORD"),
    host = os.environ.get("DB_HOST"),
    port = os.environ.get("DB_PORT")
    )

# dialect+driver://username:password@host:port/database
ENGINE = create_engine(f'postgresql+psycopg2://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_DATABASE")}')
# ENGINE = create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/postgres")


