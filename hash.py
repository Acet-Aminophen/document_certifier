import hashlib


def sha256(str1: str):
    return hashlib.sha256(str1.encode()).hexdigest()
