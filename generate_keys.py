from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import ast

rand_generator = Random.new(32).read
key = RSA.generate(1024, rand_generator) #generate pub and priv key

publickey = key.publickey()

encryptor = PKCS1_OAEP.new(publickey)

print("[+] Generating new key:")

rsa_key = key.exportKey()
print("[*] Base64 encode and host the following key:")
print(f"\n{rsa_key.decode()}")

print("\n[+] Encrypting github token...")

encrypted = encryptor.encrypt(b'PAT here')
print("[*] Put the encrypted token into the source of git_trojan.py:")
print(f'\n{encrypted}')

