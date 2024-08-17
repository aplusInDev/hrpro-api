from .auth_db import DB
from .auth import Auth


db = DB()
db.reload()

auth = Auth()
