import hashlib
from app.schemas.user_test import UserForCreate


hash_obj = hashlib.sha256()

def hash_password(user:UserForCreate) -> UserForCreate:
    user.password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    return user