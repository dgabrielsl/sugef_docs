import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from webbrowser import open as webbrowser_open
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image

class RootAuth(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ui()
        self.show()

    def start_ui(self):
        self.setWindowIcon(QIcon(f'{os.getcwd()}/icon.png'))
        self.setWindowTitle('Autorizaciones SUGEF')
        h1 = QLabel('Separar CIC + convertir IDs a PDF', alignment=Qt.AlignmentFlag.AlignCenter)
        h1.setStyleSheet('font-size: 20px;')
        h2 = QLabel('Autorizaciones SUGEF / Actualización de datos', alignment=Qt.AlignmentFlag.AlignCenter)
        h2.setStyleSheet('font-size: 14px; font-weight: bold')
        h2.setContentsMargins(0,0,0,20)
        href_1 = QPushButton('docs.google.com/spreadsheets')
        href_1.setStyleSheet('background-color: none; color: #05A; font-size: 14px; font-style: italic; text-decoration: underline; border: none;')
        href_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        href_1.clicked.connect(lambda:webbrowser_open('https://docs.google.com/spreadsheets/d/1tmVzOZzoWYPUMpmKbROUZLnRsZ5iJkG0OuX9eF7SZhw/edit?pli=1#gid=0'))
        lhref_1 = QLabel('Actualizacion-Bloqueo (Clientes para autorizar)', alignment=Qt.AlignmentFlag.AlignCenter)
        lhref_1.setStyleSheet('color: #777;')
        lhref_1.setContentsMargins(0,0,0,10)
        href_2 = QPushButton('cic.sugef.fi.cr')
        href_2.setStyleSheet('background-color: none; color: #05A; font-size: 14px; font-style: italic; text-decoration: underline; border: none;')
        href_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        href_2.clicked.connect(lambda:webbrowser_open('https://cic.sugef.fi.cr/cic/CIC.aspx'))
        lhref_2 = QLabel('SUGEF', alignment=Qt.AlignmentFlag.AlignCenter)
        lhref_2.setStyleSheet('margin-bottom: 20px; color: #777;')
        hrefs = QVBoxLayout()
        hrefs.addWidget(href_1)
        hrefs.addWidget(lhref_1)
        hrefs.addWidget(href_2)
        hrefs.addWidget(lhref_2)
        bttn_1 = QPushButton('Cargar una carpeta')
        bttn_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        bttn_1.clicked.connect(lambda:self.__open_file_dialog())
        bttn_1.clicked.connect(self.split_and_convert)
        bttn_1.setStyleSheet('margin-bottom: 30px; padding: 8px 20px; color: #39D; font-family: Segoe UI;')
        self.take_out_documents = QRadioButton('Sacar los documentos.')
        self.take_out_documents.setChecked(True)
        self.rename_each_folder = QRadioButton('Renombrar cada sub-carpeta.')
        wrap_radiobuttons = QHBoxLayout()
        wrap_radiobuttons.addWidget(self.take_out_documents)
        wrap_radiobuttons.addWidget(self.rename_each_folder)
        wrap_radiobuttons.setContentsMargins(0,0,0,5)
        bttn_2 = QPushButton('Cargar varias carpetas')
        bttn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        bttn_2.clicked.connect(lambda:self.__open_file_dialog())
        bttn_2.clicked.connect(self.split_and_convert)
        bttn_2.setStyleSheet('padding: 8px 20px; color: #39D; font-family: Segoe UI;')
        layout = QVBoxLayout()
        layout.addWidget(h1)
        layout.addWidget(h2)
        layout.addLayout(hrefs)
        layout.addWidget(bttn_1)
        layout.addLayout(wrap_radiobuttons)
        layout.addWidget(bttn_2)
        layout.setContentsMargins(30,30,30,30)
        self.setLayout(layout)

    def __open_file_dialog(self):
        self.filedialog = QFileDialog.getExistingDirectory()

    def split_and_convert(self):
            try:
                self.tod = self.take_out_documents.isChecked()
                if self.sender().text() == 'Cargar una carpeta':
                    try:
                        self.items_in_folder = os.listdir(self.filedialog)
                        self.id_items = []
                        for lf in self.items_in_folder:
                            self.items_in_folder[self.items_in_folder.index(lf)] = f'{self.filedialog}/{lf}'
                            _lf_ = lf.upper()
                            print(_lf_)
                            if _lf_.__contains__('AFF') or _lf_.__contains__('CIC'): self.readable_item = f'{self.filedialog}/{lf}'
                            elif _lf_.__contains__('ID'): self.id_items.append(f'{self.filedialog}/{lf}')
                    except Exception as e: print(f'__hint__: Root.split_and_convert()\n{e}')
                    self.__make_cic()
                    self.__make_id()
                elif self.sender().text() == 'Cargar varias carpetas':
                    self.items_in_folder = os.listdir(self.filedialog)
                    self.set = os.listdir(self.filedialog)
                    for sub_folder in self.set:
                        sub_folder_files = os.listdir(f'{self.filedialog}/{sub_folder}')
                        self.id_items = []
                        for sff in sub_folder_files:
                            _sff_ = sff.upper()
                            if _sff_.__contains__('AFF') or _sff_.__contains__('CIC'): self.readable_item = f'{self.filedialog}/{sub_folder}/{sff}'
                            elif _sff_.__contains__('ID'): self.id_items.append(f'{self.filedialog}/{sub_folder}/{sff}')
                        self.preserve_fd = self.filedialog
                        self.filedialog = f'{self.filedialog}/{sub_folder}'
                        self.__make_cic()
                        self.__make_id()
                        if self.rename_each_folder.isChecked(): os.rename(f'{self.filedialog}', f'{self.preserve_fd}/{self.identif} {self.name}')
                        self.del_folder = []
                        self.del_folder.append(self.filedialog)
                        self.filedialog = self.preserve_fd
                    if self.tod:
                        for df in self.del_folder:
                            try: os.chmod(f'{df}', 0o777)
                            except: pass
            except Exception as e: print(f'__hint__: RootAuth.split_and_convert()\n{e}')

    def __make_cic(self):
        try:
            _pdf = open(self.readable_item, 'rb')
            self._reader = PdfReader(_pdf)
            self._doc_size = self._reader.pages.__len__()
            self._content = self._reader.pages[0].extract_text().split('\n')
            for line in self._content:
                if line.__contains__('Yo,') and line.__contains__('identificac') and line.__contains__('autorizo'):
                    line = line.split(',')
                    self.name = line[1]
                    self.name = self.name.split(' ')
                    for n in self.name:
                        if n == '' or n == ' ': self.name.pop(self.name.index(n))
                    self.name = ' '.join(self.name).upper()
                    identif = line[2]
                    identif = identif.split(' ')
                    identif = identif[-1]
                    self.identif = identif
                    self._content = line
                    break
            _writer = PdfWriter()
            _writer.add_page(self._reader.pages[0])
            _writer.add_page(self._reader.pages[-2])
            _writer.add_page(self._reader.pages[-1])
            if self.sender().text() == 'Cargar varias carpetas':
                if self.tod: output_name = f'{self.preserve_fd}/{self.identif} CIC.pdf'
                else: output_name = f'{self.filedialog}/{self.identif} CIC.pdf'
            else: output_name = f'{self.filedialog}/{self.identif} CIC.pdf'
            with open(self.readable_item, 'wb') as f:
                _writer.write(f)
                f.close()
            _pdf.close()
            os.rename(self.readable_item, output_name)
        except Exception as e: print(f'__hint__: RootAuth.__make_cic()\n{e}')

    def __make_id(self):
        try:
            if len(self.id_items) > 1:
                _merge = PdfMerger()
                if self.id_items[0].__contains__('.pdf') or self.id_items[0].__contains__('.PDF'):
                    _merge.append(self.id_items[0])
                    _merge.append(self.id_items[1])
                    if self.tod: output_name = f'{self.preserve_fd}/{self.identif} ID.pdf'
                    else: output_name = f'{self.filedialog}/{self.identif} ID.pdf'
                    with open(output_name, 'wb') as f:
                        _merge.write(f)
                        _merge.close()
                        f.close()
                else:
                    _img = Image.open(self.id_items[0])
                    _img = _img.convert('RGB')
                    _img.save(f'{self.filedialog}/ID1.pdf')
                    _img = Image.open(self.id_items[1])
                    _img = _img.convert('RGB')
                    _img.save(f'{self.filedialog}/ID2.pdf')
                    _merge.append(f'{self.filedialog}/ID1.pdf')
                    _merge.append(f'{self.filedialog}/ID2.pdf')
                    if self.sender().text() == 'Cargar varias carpetas':
                        if self.tod: output_name = f'{self.preserve_fd}/{self.identif} ID.pdf'
                        else: output_name = f'{self.filedialog}/{self.identif} ID.pdf'
                    else: output_name = f'{self.filedialog}/{self.identif} ID.pdf'
                    with open(output_name, 'wb') as f:
                        _merge.write(f)
                        _merge.close()
                        f.close()
                try: os.remove(self.id_items[0]); os.remove(self.id_items[1])
                except: pass
                try: os.remove(f'{self.filedialog}/ID1.pdf'); os.remove(f'{self.filedialog}/ID2.pdf')
                except: pass
            else:
                if self.sender().text() == 'Cargar varios documentos': self.working_path = self.preserve_fd
                else: self.working_path = self.filedialog

                if self.id_items[0].__contains__('.pdf') or self.id_items[0].__contains__('.PDF'):
                    if self.tod: os.rename(self.id_items[0], f'{self.working_path}/{self.identif} ID.pdf')
                    else: os.rename(self.id_items[0], f'{self.filedialog}/{self.identif} ID.pdf')
                else:
                    _img = Image.open(self.id_items[0])
                    _img = _img.convert('RGB')
                    if self.tod: _img.save(f'{self.working_path}/{self.identif} ID.pdf')
                    else: _img.save(f'{self.filedialog}/{self.identif} ID.pdf')
                    os.remove(self.id_items[0])
        except Exception as e: print(f'__hint__: RootAuth.__make_id()\n{e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RootAuth()
    sys.exit(app.exec())