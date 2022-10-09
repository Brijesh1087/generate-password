from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)
f = Fernet(key)
en = f.encrypt("world".encode())
print(en[2:-2])
de = f.decrypt(en)
print(de.decode())
# print("hello".encode())