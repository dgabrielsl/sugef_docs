# Libraries.
import os, sys

# Import all.
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Sefl-build modules.
import autorizaciones

class Root(QMainWindow):
    def __init__(self):
        os.system('cls')
        super().__init__()
        self.cn = f'{os.getcwd()}\\assets\\'
        self.start_app()
        self.show()

    def start_app(self):
        self.setWindowIcon(QIcon(f'{self.cn}icon.png'))
        self.setWindowTitle('Financiera Multimoney')
        self.setMinimumWidth(350)
        self.setMinimumHeight(400)

        menu = self.menuBar()
        file_menu = menu.addMenu('&Archivo')
        file_1 = file_menu.addAction('Cerrar sesión')
        file_1.setIcon(QIcon(f'{self.cn}logout.png'))
        file_1.setDisabled(True)
        file_2 = file_menu.addAction('Salir')
        file_2.setIcon(QIcon(f'{self.cn}exit.png'))
        file_2.triggered.connect(self.deleteLater)
        sett_menu = menu.addMenu('&Configuración')
        sett_menu.setDisabled(True)
        docs_menu = menu.addMenu('&Documentación')
        docs_menu.setDisabled(True)

        # Auth.RootAuth()
        # Build the CIC from the affidavit and convert image files to PDF.
        nw_root_auth = QPushButton('Autorizaciones SUGEF / Actualización de datos')
        nw_root_auth.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        nw_root_auth.setStyleSheet('padding: 12px; font-size: 15px;')
        nw_root_auth.clicked.connect(lambda:autorizaciones.RootAuth())

        self.main_widget = QWidget()
        lyt = QVBoxLayout()
        lyt.setContentsMargins(50,50,50,50)
        lyt.addWidget(nw_root_auth)
        self.main_widget.setLayout(lyt)
        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Root()
    app.exit(app.exec())