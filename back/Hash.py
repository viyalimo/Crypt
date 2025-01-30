import hashlib

class Hash:
    def hash_data(self, sha: int = 256, data: str = None, file: str = None) -> str:
        if sha == 256:
            hash_object = hashlib.sha256()
        elif sha == 512:
            hash_object = hashlib.sha512()
        else:
            raise ValueError("Поддерживаются только SHA-256 и SHA-512.")

        if file:
            try:
                with open(file, 'rb') as f:
                    while chunk := f.read(4096):  # Чтение файла блоками по 4096 байт
                        hash_object.update(chunk)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл '{file}' не найден.")
        elif data:
            hash_object.update(data.encode('utf-8'))
        else:
            raise ValueError("Необходимо указать либо строку, либо файл.")

        return hash_object.hexdigest()