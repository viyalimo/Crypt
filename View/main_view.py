import os.path

from flet import *
from back.Podpis import FileWithSignatureAndPublicKey
from back.AES import AES
from flet_route import Params, Basket
import concurrent.futures
from back.Game import SnakeGame


class MainPage(AES, FileWithSignatureAndPublicKey):
    def __init__(self):
        super().__init__()

    def view(self, page: Page, params: Params, basket: Basket):

        content_container = Column(controls=[Row(controls=[Text("Начать")], alignment=MainAxisAlignment.CENTER)],
                                   alignment=MainAxisAlignment.CENTER, expand=True)

        def on_navigation_change(index):
            if index == 0:
                shifr_container()
            elif index == 1:
                shifr_folder()
            elif index == 2:
                deshifr_file()
            elif index == 3:
                make_podpic()
            elif index == 4:
                check_podpic()
            elif index == 5:
                style_revert()
            elif index == 6:
                start_game()

        def start_game():
            content_container.controls.clear()
            SnakeGame(content_container)

        def shifr_next_password(path):
            content_container.controls.clear()
            path_file = path
            pb = ProgressBar(value=0.0, visible=False, width=400, height=5)  # Прогресс-бар

            def back(e):
                shifr_container()

            def next(e):
                if shifr_enter_password.value:
                    if len(shifr_enter_password.value) >= 10:
                        out_path = path_file + ".cont"
                        pb.value = 0.0
                        pb.visible = True
                        page.update()

                        def encryption_task():
                            try:
                                result = self.encrypt_file(path_file, shifr_enter_password.value, out_path, pb=pb)
                                pb.visible = False
                                page.update()

                                if result:
                                    page.snack_bar = SnackBar(
                                        content=Row(
                                            [Text(f"Контейнер успешно создан в {out_path}", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                        bgcolor=colors.GREEN,
                                    )
                                    page.snack_bar.open = True
                                    shifr_container()
                                else:
                                    page.snack_bar = SnackBar(
                                        content=Row(
                                            [Text(f"Попробуйте выбрать другую директорию", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                        bgcolor=colors.RED,
                                    )
                                    page.snack_bar.open = True
                                    shifr_container()
                            except Exception as ex:
                                pb.visible = False
                                page.snack_bar = SnackBar(
                                    content=Row([Text("Произошла ошибка при шифровании", color='white')],
                                                alignment=MainAxisAlignment.CENTER),
                                    bgcolor=colors.RED,
                                )
                                page.snack_bar.open = True
                                shifr_container()

                        executor = concurrent.futures.ThreadPoolExecutor()
                        executor.submit(encryption_task)

                    else:
                        page.snack_bar = SnackBar(
                            content=Row([Text("Пароль должен содержать минимум 10 символов", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.RED,
                        )
                        page.snack_bar.open = True
                        page.update()
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Введите пароль!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()

            shifr_enter_password = TextField(hint_text="Введите пароль!", width=400, password=True,
                                             can_reveal_password=True)

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))
            back_btn = Container(content=ElevatedButton(text="Назад", on_click=lambda e: back(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                shifr_enter_password,
                                pb,
                                Row(
                                    controls=[
                                        back_btn,
                                        next_btn,
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,
            )
            content_container.controls.append(col)
            page.update()

        def shifr_container():
            content_container.controls.clear()

            def on_dialog_result(e):
                shifr_enter_path.value = e.path
                page.update()

            def next(e):
                if shifr_enter_path.value:
                    shifr_next_password(shifr_enter_path.value)
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Выберите путь к файлу!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,

                    )
                    page.snack_bar.open = True
                    page.update()

            file_peacker = FilePicker(on_result=lambda e: on_dialog_result(e))
            page.overlay.append(file_peacker)
            shifr_enter_path = TextField(hint_text="Расположение контейнера и имя без расширения", width=400,
                                         suffix_icon=IconButton(icon=icons.FILE_DOWNLOAD,
                                                                on_click=lambda e: file_peacker.save_file()))

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Создание криптоконтейнера", text_align=TextAlign.CENTER),
                                shifr_enter_path,
                                file_peacker,
                                next_btn,
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,

            )
            content_container.controls.append(col)
            page.update()

        def deshifr_next_password(path):
            content_container.controls.clear()
            path_file = path
            pb = ProgressBar(value=0.0, visible=False, width=400, height=5)  # Прогресс-бар

            def back(e):
                deshifr_file()

            def shifr_file(e):
                open_path = path_file[:-5]
                pb.value = 0.0  # Сброс прогресса
                pb.visible = True
                page.update()
                password = shifr_enter_password.value
                shifr_enter_password.value = ""
                shifr_enter_password.update()
                page.update()

                # Фоновая задача для шифрования
                def encryption_task():
                    try:
                        result = self.encrypt_file(open_path, password, path_file, pb=pb)
                        pb.visible = False
                        page.update()
                        if result:
                            page.snack_bar = SnackBar(
                                content=Row([Text(f"Файл успешно зашифрован", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                bgcolor=colors.GREEN,
                            )
                            navigation_bar.visible = True
                            page.snack_bar.open = True
                            page.update()
                            deshifr_file()
                        else:
                            page.snack_bar = SnackBar(
                                content=Row([Text(f"Произошла ошибка при шифровании!", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                bgcolor=colors.RED,
                            )
                            page.snack_bar.open = True
                            page.update()
                    except Exception as ex:
                        pb.visible = False
                        page.snack_bar = SnackBar(
                            content=Row([Text("Произошла ошибка при шифровании", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.RED,
                        )
                        page.snack_bar.open = True

                # Запуск в отдельном потоке
                executor = concurrent.futures.ThreadPoolExecutor()
                executor.submit(encryption_task)

            def next(e):
                if shifr_enter_password.value:
                    out_path = path_file[:-5]
                    pb.value = 0.0  # Сброс прогресса
                    pb.visible = True
                    page.update()

                    # Фоновая задача для расшифровки
                    def decryption_task():
                        try:
                            result = self.decrypt_file(path_file, shifr_enter_password.value, out_path, pb=pb)
                            pb.visible = False
                            page.update()

                            if result:
                                next_btn.visible = False
                                shefr.visible = True
                                back_btn.visible = False
                                os.startfile(out_path)
                                page.snack_bar = SnackBar(
                                    content=Row(
                                        [Text(f"Контейнер расшифрован и находится в файле {out_path}", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                                    bgcolor=colors.GREEN,
                                )
                                page.snack_bar.open = True
                                page.update()
                            else:
                                page.snack_bar = SnackBar(
                                    content=Row(
                                        [Text("Ошибка расшифровки контейнера", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                                    bgcolor=colors.RED,
                                )
                                page.snack_bar.open = True
                                page.update()

                        except Exception as ex:
                            pb.visible = False
                            page.snack_bar = SnackBar(
                                content=Row([Text("Произошла ошибка при расшифровке", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                bgcolor=colors.RED,
                            )
                            page.snack_bar.open = True

                    # Запуск в отдельном потоке
                    executor = concurrent.futures.ThreadPoolExecutor()
                    executor.submit(decryption_task)

                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Введите пароль!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()

            shifr_enter_password = TextField(hint_text="Введите пароль!", width=400, password=True,
                                             can_reveal_password=True)

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))
            back_btn = Container(content=ElevatedButton(text="Назад", on_click=lambda e: back(e)),
                                 alignment=Alignment(0, 0))

            shefr = Container(content=ElevatedButton(text="Закрыть контейнер", on_click=lambda e: shifr_file(e)),
                              alignment=Alignment(0, 0), visible=False)

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                shifr_enter_password,
                                pb,  # Прогресс-бар
                                Row(
                                    controls=[
                                        back_btn,
                                        next_btn,
                                        shefr
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,
            )
            content_container.controls.append(col)
            page.update()

        def deshifr_file():
            content_container.controls.clear()

            def on_dialog_result(e):
                shifr_enter_path.value = e.files[0].path
                page.update()

            def next(e):
                if shifr_enter_path.value:
                    deshifr_next_password(shifr_enter_path.value)
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Выберите путь к файлу!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,

                    )
                    page.snack_bar.open = True
                    page.update()

            file_peacker = FilePicker(on_result=lambda e: on_dialog_result(e))
            page.overlay.append(file_peacker)
            shifr_enter_path = TextField(hint_text="Выберите контейнер", width=400,
                                         suffix_icon=IconButton(icon=icons.FILE_DOWNLOAD,
                                                                on_click=lambda e: file_peacker.pick_files()))

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                shifr_enter_path,
                                file_peacker,
                                next_btn,
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,

            )
            content_container.controls.append(col)
            page.update()

        def check_podpic():
            content_container.controls.clear()

            def on_dialog_result(e):
                print(e.path)
                shifr_enter_path.value = e.path
                page.update()

            def next(e):
                if shifr_enter_path.value:
                    result = self.verify_signed_folder(shifr_enter_path.value)
                    if result:
                        page.snack_bar = SnackBar(
                            content=Row([Text("Подпись действительна!", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.GREEN,

                        )
                        page.snack_bar.open = True
                        page.update()
                    else:
                        page.snack_bar = SnackBar(
                            content=Row([Text("Подпись не действительна!", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.RED,

                        )
                        page.snack_bar.open = True
                        page.update()
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Выберите путь для проверки", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,

                    )
                    page.snack_bar.open = True
                    page.update()

            file_peacker = FilePicker(on_result=lambda e: on_dialog_result(e))
            page.overlay.append(file_peacker)
            shifr_enter_path = TextField(hint_text="Выберите файл для проверки", width=400,
                                         suffix_icon=IconButton(icon=icons.FILE_DOWNLOAD,
                                                                on_click=lambda e: file_peacker.get_directory_path()))

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Проверка файла с цифровой подписью", text_align=TextAlign.CENTER),
                                shifr_enter_path,
                                file_peacker,
                                next_btn,
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,

            )
            content_container.controls.append(col)
            page.update()

        def make_file_with_podpis(path, file_name):
            folder_path = file_name.split(".")[0]

            result = FileWithSignatureAndPublicKey().sign_file_and_save(path, folder_path)
            if result:
                page.snack_bar = SnackBar(
                    content=Row(
                        [Text(f"Файл успешно подписан и сохранён в \n {folder_path}", color='white')],
                        alignment=MainAxisAlignment.CENTER),
                    bgcolor=colors.GREEN,
                )
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = SnackBar(
                    content=Row([Text(f"Не удалось подписать файл!",
                                      color='white')],
                                alignment=MainAxisAlignment.CENTER),
                    bgcolor=colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        def make_podpic():
            content_container.controls.clear()

            def on_dialog_result(e):
                shifr_enter_path.value = e.files[0].path
                page.update()

            def next(e):
                if shifr_enter_path.value:
                    folder_name = shifr_enter_path.value.split(".")[0]
                    make_file_with_podpis(shifr_enter_path.value, file_name=shifr_enter_path.value.split("/")[-1])
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Выберите путь к файлу!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,

                    )
                    page.snack_bar.open = True
                    page.update()

            file_peacker = FilePicker(on_result=lambda e: on_dialog_result(e))
            page.overlay.append(file_peacker)
            shifr_enter_path = TextField(hint_text="Путь к файлу", width=400,
                                         suffix_icon=IconButton(icon=icons.FILE_DOWNLOAD,
                                                                on_click=lambda e: file_peacker.pick_files()))

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Создание подписи", text_align=TextAlign.CENTER),
                                shifr_enter_path,
                                file_peacker,
                                Row(
                                    [
                                        next_btn
                                    ]
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,

            )
            content_container.controls.append(col)
            page.update()

        def shifr_folder_password(path):
            content_container.controls.clear()
            path_file = path
            pb = ProgressBar(value=0.0, visible=False, width=400, height=5)  # Прогресс-бар

            def back(e):
                shifr_folder()

            def next(e):
                if shifr_enter_password.value:
                    if len(shifr_enter_password.value) >= 10:
                        out_path = path_file + ".cont"
                        pb.value = 0.0
                        pb.visible = True
                        page.update()

                        def encryption_task():
                            try:
                                result = self.encrypt_file(path_file, shifr_enter_password.value, out_path, pb=pb)
                                pb.visible = False
                                page.update()

                                if result:
                                    page.snack_bar = SnackBar(
                                        content=Row([Text(f"Контейнер успешно создан в {out_path}", color='white')],
                                                    alignment=MainAxisAlignment.CENTER),
                                        bgcolor=colors.GREEN,
                                    )
                                    page.snack_bar.open = True
                                    page.update()
                                    shifr_container()
                                else:
                                    page.snack_bar = SnackBar(
                                        content=Row([Text("Попробуйте выбрать другую директорию", color='white')],
                                                    alignment=MainAxisAlignment.CENTER),
                                        bgcolor=colors.RED,
                                    )
                                    page.snack_bar.open = True
                                    page.update()
                                    shifr_container()
                            except Exception as ex:
                                pb.visible = False
                                page.snack_bar = SnackBar(
                                    content=Row([Text("Произошла ошибка при шифровании", color='white')],
                                                alignment=MainAxisAlignment.CENTER),
                                    bgcolor=colors.RED,
                                )
                                page.snack_bar.open = True

                        executor = concurrent.futures.ThreadPoolExecutor()
                        executor.submit(encryption_task)

                    else:
                        page.snack_bar = SnackBar(
                            content=Row([Text("Пароль должен содержать минимум 10 символов", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.RED,
                        )
                        page.snack_bar.open = True
                        page.update()
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Введите пароль!", color='white')],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()

            def shifr_file(e):
                open_path = path_file
                pb.value = 0.0
                pb.visible = True
                page.update()

                password = shifr_enter_password.value
                shifr_enter_password.value = ""
                shifr_enter_password.update()
                page.update()

                def encryption_task():
                    try:
                        result = self.encrypt_file(open_path, password, path_file, pb=pb)
                        pb.visible = False
                        page.update()

                        if result:
                            page.snack_bar = SnackBar(
                                content=Row([Text(f"Файл успешно зашифрован", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                bgcolor=colors.GREEN,
                            )
                            page.snack_bar.open = True
                            page.update()
                            shifr_folder()
                        else:
                            page.snack_bar = SnackBar(
                                content=Row([Text(f"Произошла ошибка при шифровании!", color='white')],
                                            alignment=MainAxisAlignment.CENTER),
                                bgcolor=colors.RED,
                            )
                            page.snack_bar.open = True
                            page.update()
                    except Exception as ex:
                        pb.visible = False
                        page.snack_bar = SnackBar(
                            content=Row([Text("Произошла ошибка при шифровании", color='white')],
                                        alignment=MainAxisAlignment.CENTER),
                            bgcolor=colors.RED,
                        )
                        page.snack_bar.open = True

                executor = concurrent.futures.ThreadPoolExecutor()
                executor.submit(encryption_task)

            shifr_enter_password = TextField(hint_text="Введите пароль!", width=400, password=True,
                                             can_reveal_password=True)

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))
            back_btn = Container(content=ElevatedButton(text="Назад", on_click=lambda e: back(e)),
                                 alignment=Alignment(0, 0))

            shefr = Container(content=ElevatedButton(text="Закрыть контейнер", on_click=lambda e: shifr_file(e)),
                              alignment=Alignment(0, 0), visible=False)

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                shifr_enter_password,
                                pb,
                                Row(
                                    controls=[
                                        back_btn,
                                        next_btn,
                                        shefr
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,
            )
            content_container.controls.append(col)
            page.update()

        def shifr_folder():
            content_container.controls.clear()

            def on_dialog_result(e):
                shifr_enter_path.value = e.path
                page.update()

            def next(e):
                if shifr_enter_path.value:
                    shifr_folder_password(shifr_enter_path.value)
                else:
                    page.snack_bar = SnackBar(
                        content=Row([Text("Выберите путь к файлу!", text_align=TextAlign.CENTER)],
                                    alignment=MainAxisAlignment.CENTER),
                        bgcolor=colors.RED,

                    )
                    page.snack_bar.open = True
                    page.update()

            file_peacker = FilePicker(on_result=lambda e: on_dialog_result(e))
            page.overlay.append(file_peacker)
            shifr_enter_path = TextField(hint_text="Путь к папке", width=400,
                                         suffix_icon=IconButton(icon=icons.FILE_DOWNLOAD,
                                                                on_click=lambda e: file_peacker.get_directory_path()))

            next_btn = Container(content=ElevatedButton(text="Далее", on_click=lambda e: next(e)),
                                 alignment=Alignment(0, 0))

            col = Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Зашифровать существующий файл"),
                                shifr_enter_path,
                                file_peacker,
                                next_btn,
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=Alignment(0, 0),
                expand=True,

            )
            content_container.controls.append(col)
            page.update()

        def style_revert():
            if page.theme_mode == ThemeMode.DARK:
                page.theme_mode = ThemeMode.LIGHT
                navigation_bar.destinations[5].icon = icons.DARK_MODE_OUTLINED
            else:
                page.theme_mode = ThemeMode.DARK
                navigation_bar.destinations[5].icon = icons.SUNNY
            page.update()

        navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(icon=icons.ENHANCED_ENCRYPTION_OUTLINED, label="Создать криптоконтейнер"),
                NavigationBarDestination(icon=icons.LOCK_OUTLINED, label="Зашифровать файл"),
                NavigationBarDestination(icon=icons.LOCK_OPEN_OUTLINED, label="Открыть криптоконтейнер"),
                NavigationBarDestination(icon=icons.DOWNLOAD_DONE, label="Цифровая подпись"),
                NavigationBarDestination(icon=icons.DOCUMENT_SCANNER, label="Проверить подлинность"),
                NavigationBarDestination(icon=Icons.DARK_MODE_OUTLINED, label="Стиль приложения"),
                NavigationBarDestination(icon=Icons.GAMEPAD,
                                         label="Играть",
                                         disabled=True,
                                         visible=False
                                         ),
            ],
            selected_index=0,
            on_change=lambda e: on_navigation_change(e.control.selected_index),
        )

        return View("/", controls=[navigation_bar, content_container])
