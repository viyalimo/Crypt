

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from Crypto.PublicKey import RSA

from back.FoldertoCont import FolderToCont
from back.Hash import Hash
import gc

class AES(Hash, FolderToCont):
    def __init__(self):
        super().__init__()
        self.private_key = None

    def _secure_delete(self, obj):

        if isinstance(obj, bytes):
            mutable_obj = bytearray(obj)
            for i in range(len(mutable_obj)):
                mutable_obj[i] = 0
        elif isinstance(obj, bytearray):
            for i in range(len(obj)):
                obj[i] = 0
        elif hasattr(obj, '__dict__'):
            for attr in list(obj.__dict__.keys()):
                setattr(obj, attr, None)
        del obj
        gc.collect()

    def ecrypt_password(self, hash: str, private_key: bytes, pb=None):

        hash_key = hash.encode('utf-8')

        salt = b'some_fixed_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = kdf.derive(hash_key)
        if pb:
            pb.value += 0.2
            pb.update()

        iv = os.urandom(16)
        if pb:
            pb.value += 0.2
            pb.update()


        cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()


        ciphertext = encryptor.update(private_key) + encryptor.finalize()
        if pb:
            pb.value += 0.2
            pb.update()

        return base64.b64encode(iv + ciphertext)

    def encrypt_file(self, file: str, key: str, output_file: str, pb=None):
        try:
            self.folder_to_cont(file, output_file)
            if pb:
                pb.value += 0.1
                pb.update()


            key_RSA = RSA.generate(2048)
            private_key = key_RSA.export_key()
            public_key = key_RSA.publickey().export_key()
            if pb:
                pb.value += 0.1
                pb.update()

            encrypted_private_key = self.ecrypt_password(hash=key, private_key=private_key, pb=pb)

            salt = b'some_fixed_salt'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            derived_key = kdf.derive(key.encode('utf-8'))
            if pb:
                pb.value += 0.1
                pb.update()

            with open(output_file, 'rb') as f:
                plaintext = f.read()
            if pb:
                pb.value += 0.1
                pb.update()

            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            if pb:
                pb.value += 0.1
                pb.update()

            with open(output_file, 'wb') as out_f:
                out_f.write(base64.b64encode(encrypted_private_key) + b'\n')
                out_f.write(base64.b64encode(iv + ciphertext))
            if pb:
                pb.value += 0.1
                pb.update()

            return True
        except Exception as e:
            return False
        finally:
            self._secure_delete(derived_key)
            self._secure_delete(private_key)
            self._secure_delete(encrypted_private_key)
            self._secure_delete(plaintext)
            self._secure_delete(ciphertext)
            self._secure_delete(iv)

    def decrypt_password(self, hash: str, encrypted_data: bytes, pb=None):
        hash_key = hash.encode('utf-8')
        salt = b'some_fixed_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = kdf.derive(hash_key)
        if pb:
            pb.value += 0.2
            pb.update()

        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        if pb:
            pb.value += 0.2
            pb.update()

        cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        if pb:
            pb.value += 0.2
            pb.update()

        return plaintext

    def decrypt_file(self, encrypted_file: str, key: str, output_file: str, pb=None):
        try:
            with open(encrypted_file, 'rb') as f:
                lines = f.readlines()

            encrypted_private_key = base64.b64decode(lines[0].strip())
            encrypted_data = base64.b64decode(lines[1].strip())
            if pb:
                pb.value += 0.2
                pb.update()

            private_key = self.decrypt_password(hash=key, encrypted_data=encrypted_private_key, pb=pb)

            salt = b'some_fixed_salt'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            derived_key = kdf.derive(key.encode('utf-8'))
            if pb:
                pb.value += 0.2
                pb.update()

            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

            cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            if pb:
                pb.value += 0.2
                pb.update()

            with open(encrypted_file, 'wb') as f:
                f.write(plaintext)

            self.cont_to_folder(encrypted_file, output_file)
            if pb:
                pb.value = 1.0
                pb.update()

            return True
        except Exception as e:
            return False

