import hashlib

str1 = "test1"

print(hashlib.sha256(str1.encode()).hexdigest())