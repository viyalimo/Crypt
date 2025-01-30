import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import utils


class FileWithSignatureAndPublicKey:
    BUFFER_SIZE = 64 * 1024  # 64 KB

    def __init__(self):
        # Генерация ключей
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def export_public_key(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def sign_file_and_save(self, input_file: str, output_folder: str):
        try:
            if not os.path.exists(input_file):
                raise f"Файл {input_file} не найден!"

            os.makedirs(output_folder, exist_ok=True)

            hash_algorithm = hashes.SHA256()
            digest = hashes.Hash(hash_algorithm)
            with open(input_file, "rb") as file:
                while chunk := file.read(self.BUFFER_SIZE):
                    digest.update(chunk)
            hashed_file = digest.finalize()

            signature = self.private_key.sign(
                hashed_file,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(hashes.SHA256())
            )

            file_name = os.path.basename(input_file)
            signed_file = os.path.join(output_folder, file_name)
            public_key_file = os.path.join(output_folder, "public_key.txt")
            signature_file = os.path.join(output_folder, f"{file_name}.signature")

            with open(signed_file, "wb") as sf:
                with open(input_file, "rb") as file:
                    sf.write(file.read())

            with open(public_key_file, "wb") as pkf:
                pkf.write(self.export_public_key())

            with open(signature_file, "wb") as sigf:
                sigf.write(signature)

            return True
        except Exception as e:
            return False

    def verify_signed_folder(self, folder: str) -> bool:

        try:
            files = os.listdir(folder)

            public_key_file = None
            for file in files:
                if file == "public_key.txt":
                    public_key_file = os.path.join(folder, file)
                    break

            if not public_key_file:
                raise FileNotFoundError("Публичный ключ не найден!")

            data_file = None
            signature_file = None
            for file in files:
                if file != "public_key.txt" and not file.endswith(".signature"):
                    data_file = os.path.join(folder, file)
                elif file.endswith(".signature"):
                    signature_file = os.path.join(folder, file)

            if not data_file or not signature_file:
                raise FileNotFoundError("Не найдены данные или подпись!")

            with open(public_key_file, "rb") as pkf:
                public_key = serialization.load_pem_public_key(pkf.read())

            with open(signature_file, "rb") as sigf:
                signature = sigf.read()

            hash_algorithm = hashes.SHA256()
            digest = hashes.Hash(hash_algorithm)
            with open(data_file, "rb") as df:
                while chunk := df.read(self.BUFFER_SIZE):
                    digest.update(chunk)
            hashed_file = digest.finalize()

            public_key.verify(
                signature,
                hashed_file,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(hashes.SHA256())
            )
            return True
        except Exception as e:
            return False



