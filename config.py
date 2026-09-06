import os
from urllib.parse import quote_plus

class Config:
    DB_USER = os.getenv("DB_USER", "root")
    # quote_plus safely encodes special characters like '@' in passwords
    DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "mysql@rajiv"))
    DB_HOST = os.getenv("DB_HOST", "mysql-container2")
    DB_NAME = os.getenv("DB_NAME", "flask_demo2")

    if os.getenv("TESTING") == "True":
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False