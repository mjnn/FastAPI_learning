import hashlib

hash_obj = hashlib.sha256()

def hash_password(password:str):
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hashed_password