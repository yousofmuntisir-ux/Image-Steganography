
import os
import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )

    return kdf.derive(password.encode("utf-8"))

def encrypt_message(message, password):
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    aes = AESGCM(key)

    ciphertext = aes.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    data = salt + nonce + ciphertext

    return base64.urlsafe_b64encode(data).decode("ascii")

def decrypt_message(encrypted_message, password):
    data = base64.urlsafe_b64decode(encrypted_message)

    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")