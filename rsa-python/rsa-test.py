from rsa import *

keys = generate_keys()
encrypted = encrypt('testing...', keys['n'], keys['e'])
print(encrypted)
decrypted = decrypt(encrypted, keys['n'], keys['d'])
print(decrypted)