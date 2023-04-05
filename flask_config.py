from config import settings
import os

SQLALCHEMY_DATABASE_URI = settings.DB_CONNECT
SECRET_KEY = settings.SECRET_KEY
UPLOAD_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'uploads'
)