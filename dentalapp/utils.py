import hashlib


def hash_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()

def is_image(file):
    return file.lower().endswith(('.jpg', '.jpeg', '.png'))