# from cryptography.fernet import Fernet, MultiFernet

# key1 = Fernet.generate_key()
# key2 = Fernet.generate_key()

# f = MultiFernet([key1, key2])

# message = Fernet.generate_key()
# message = str(message).encode('utf-8')
# k = f.encrypt(message)

# print("k",k)

from cryptography.fernet import Fernet, MultiFernet
key1 = Fernet(Fernet.generate_key())
key2 = Fernet(Fernet.generate_key())
f = MultiFernet([key1, key2])
token = f.encrypt(b"Secret message!")
f.decrypt(token)
