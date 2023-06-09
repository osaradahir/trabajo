from cryptography.fernet import Fernet

# Generar una clave secreta con Fernet
clave = Fernet.generate_key()
cipher_suite = Fernet(clave)