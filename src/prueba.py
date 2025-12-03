#prueba.py
from utils.seguridad import hash_password, verificar_password

hash_test = hash_password("admin123")
print("HASH:", hash_test)
print("Coincide:", verificar_password(hash_test, "admin123"))
