import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt


class Page(QWidget):
    def __init__(self, title, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Вы на странице: {title}"))
        back_button = QPushButton("Назад в меню")
        back_button.clicked.connect(go_back_callback)
        layout.addWidget(back_button)
        self.setLayout(layout)

        # TODO add here requests all from example with requests
        # use method show_allert_and_return if critical
        # use method show_allert if warning
        # self.show_alert_and_return()

    def showEvent(self, event):
        # Only example
        super().showEvent(event)
        self.show_alert()

    def show_alert_and_return(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("Внимание")
        alert.setText("Вы открыли Страницу 1. Возврат в главное меню.")
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.buttonClicked.connect(self.go_back_callback)
        alert.exec()

    def show_alert(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("Внимание")
        alert.setText("Вы открыли Страницу 1. Возврат в главное меню.")
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Адаптивное меню")
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_page = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(40, 40, 40, 40)
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Выберите страницу:")
        label.setStyleSheet("color: white; font-size: 20px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(label)

        self.pages = {}
        page_data = [
            ("Страница 1", "icon1.png"),
            ("Страница 2", "icon2.png"),
            ("Страница 3", "icon3.png")
        ]

        for name, icon_path in page_data:
            btn = QPushButton(name)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(32, 32))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 100);
                    color: white;
                    font-size: 16px;
                    padding: 10px;
                    border: 1px solid white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 50);
                }
            """)
            btn.clicked.connect(lambda checked, n=name: self.show_page(n))
            menu_layout.addWidget(btn)

            page = Page(name, self.go_back)
            self.pages[name] = page
            self.stack.addWidget(page)

        self.menu_page.setLayout(menu_layout)
        self.menu_page.setObjectName("menuPage")
        self.menu_page.setStyleSheet("""
            QWidget#menuPage {
                background-image: url("background.jpg");
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        self.stack.addWidget(self.menu_page)
        self.stack.setCurrentWidget(self.menu_page)

    def show_page(self, name):
        self.stack.setCurrentWidget(self.pages[name])

    def go_back(self):
        self.stack.setCurrentWidget(self.menu_page)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
