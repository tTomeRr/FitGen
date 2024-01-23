import os

class Config:
    SECRET_KEY = "Sachin"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5433/flex"