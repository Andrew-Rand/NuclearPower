# import sys
# import asyncio
# import aiohttp
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton,
#     QTextEdit, QLineEdit, QLabel
# )
# from PyQt6.QtCore import QEvent
# from qasync import QEventLoop, asyncSlot
#
# class RequestApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("GET и POST с автообновлением")
#         self.setGeometry(300, 300, 600, 500)
#         self.running = False  # флаг для цикла
#
#         layout = QVBoxLayout()
#
#         # 🔹 Поля для POST-параметров
#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Имя")
#
#         self.age_input = QLineEdit()
#         self.age_input.setPlaceholderText("Возраст")
#
#         layout.addWidget(QLabel("Параметры для POST-запроса:"))
#         layout.addWidget(self.name_input)
#         layout.addWidget(self.age_input)
#
#         # 🔹 Кнопки GET и POST
#         self.get_button = QPushButton("Отправить GET-запрос вручную")
#         self.post_button = QPushButton("Отправить POST-запрос")
#
#         layout.addWidget(self.get_button)
#         layout.addWidget(self.post_button)
#
#         # 🔹 Поле вывода результата
#         self.result_area = QTextEdit()
#         self.result_area.setReadOnly(True)
#         layout.addWidget(QLabel("Результат запроса:"))
#         layout.addWidget(self.result_area)
#
#         self.setLayout(layout)
#
#         # 🔹 Подключение сигналов
#         self.get_button.clicked.connect(self.send_get)
#         self.post_button.clicked.connect(self.send_post)
#
#     def showEvent(self, event: QEvent):
#         super().showEvent(event)
#         if not self.running:
#             self.running = True
#             asyncio.get_event_loop().create_task(self.auto_update())
#             # TODO: cancel it if close widnow
#
#     async def auto_update(self):
#         while self.running:
#             await self.send_get()
#             await asyncio.sleep(1)
#
#     @asyncSlot()
#     async def send_get(self):
#         url = "https://httpbin.org/get"
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url) as response:
#                     data = await response.text()
#                     self.result_area.setText(data)
#         except Exception as e:
#             self.result_area.setText(f"Ошибка GET: {e}")
#
#     @asyncSlot()
#     async def send_post(self):
#         url = "https://httpbin.org/post"
#         payload = {
#             "name": self.name_input.text(),
#             "age": self.age_input.text()
#         }
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(url, json=payload) as response:
#                     data = await response.text()
#                     self.result_area.setText(data)
#         except Exception as e:
#             self.result_area.setText(f"Ошибка POST: {e}")
#
# def main():
#     app = QApplication(sys.argv)
#     loop = QEventLoop(app)
#     asyncio.set_event_loop(loop)
#
#     window = RequestApp()
#     window.show()
#
#     with loop:
#         loop.run_forever()
#
# if __name__ == "__main__":
#     main()


import sys
import asyncio
import aiohttp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QLineEdit
)
from PyQt6.QtCore import QEvent
from qasync import QEventLoop, asyncSlot

class AutoRequestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Автообновление GET-запроса")
        self.setGeometry(300, 300, 600, 400)
        self.running = False

        layout = QVBoxLayout()

        # 🔹 Поля для POST-параметров
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.label = QLabel("Результат GET-запроса:")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        layout.addWidget(QLabel("Параметры для POST-запроса:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)

        # 🔹 Кнопки GET и POST
        self.get_button = QPushButton("Отправить GET-запрос вручную")
        self.post_button = QPushButton("Отправить POST-запрос")

        layout.addWidget(self.get_button)
        layout.addWidget(self.post_button)

        self.exit_button = QPushButton("Выход из приложения")

        layout.addWidget(self.label)
        layout.addWidget(self.result_area)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

        # 🔹 Подключение сигналов
        self.get_button.clicked.connect(self.send_get)
        self.post_button.clicked.connect(self.send_post)
        self.exit_button.clicked.connect(self.exit_app)

    def showEvent(self, event: QEvent):
        super().showEvent(event)
        if not self.running:
            self.running = True
            asyncio.get_event_loop().create_task(self.auto_update())
            # TODO: TODO: save task and cancel it on exit

    async def auto_update(self):
        while self.running:
            await self.send_get()
            await asyncio.sleep(1)

    @asyncSlot()
    async def send_get(self):
        url = "https://httpbin.org/get"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.text()
                    self.result_area.setText(data)
        except Exception as e:
            self.result_area.setText(f"Ошибка: {e}")

    @asyncSlot()
    async def send_post(self):
        url = "https://httpbin.org/post"
        payload = {
            "name": self.name_input.text(),
            "age": self.age_input.text()
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    data = await response.text()
                    self.result_area.setText(data)
        except Exception as e:
            self.result_area.setText(f"Ошибка POST: {e}")

    def exit_app(self):
        self.running = False  # остановка цикла
        QApplication.quit()   # завершение приложения

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = AutoRequestApp()
    window.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()

