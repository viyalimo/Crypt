import os
import zipfile
import tempfile
import subprocess
import shutil
import time

class FolderToCont:
    BUFFER_SIZE = 64 * 1024  # 64 KB

    @staticmethod
    def folder_to_cont(folder_path, cont_file):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with zipfile.ZipFile(cont_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    with open(file_path, 'rb') as f:
                        with zipf.open(arcname, 'w') as zf:
                            while True:
                                data = f.read(FolderToCont.BUFFER_SIZE)
                                if not data:
                                    break
                                zf.write(data)

        shutil.rmtree(folder_path)


    @staticmethod
    def cont_to_folder(cont_file, folder_path):
        """
        Extracts a single .cont file into a folder and deletes the .cont file.

        :param cont_file: Path to the .cont file.
        :param folder_path: Path for the extracted folder.
        """
        if not os.path.exists(cont_file):
            return

        os.makedirs(folder_path, exist_ok=True)

        with zipfile.ZipFile(cont_file, 'r') as zipf:
            for file_info in zipf.infolist():
                extracted_path = os.path.join(folder_path, file_info.filename)
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                with zipf.open(file_info.filename) as zf:
                    with open(extracted_path, 'wb') as f:
                        while True:
                            data = zf.read(FolderToCont.BUFFER_SIZE)
                            if not data:
                                break
                            f.write(data)

        os.remove(cont_file)

    BUFFER_SIZE = 1024

    BUFFER_SIZE = 1024

    @staticmethod
    def cont_to_temp_and_open(cont_file):
        if not os.path.exists(cont_file):
            print(f"Файл не существует: {cont_file}")
            return

        temp_folder = tempfile.mkdtemp()


        try:
            with zipfile.ZipFile(cont_file, 'r') as zipf:
                zipf.extractall(temp_folder)

            new_file_path = os.path.join(temp_folder, "example.txt")
            with open(new_file_path, "w") as f:
                f.write("Это пример содержимого файла.")

            explorer_process = subprocess.Popen(f'explorer {temp_folder}', shell=True)

            explorer_process.wait()

            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

        except Exception as e:

            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder, ignore_errors=True)
