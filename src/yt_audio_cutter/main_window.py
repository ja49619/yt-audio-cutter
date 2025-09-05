from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from yt_dlp import YoutubeDL

from .cutter import cut_and_convert_to_mp3
from .downloader import download_audio
from .main_window_ui import Ui_MainWindow  # Импорт сгенерированного класса
from .utils import is_valid_url, video_exists


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Пример привязки кнопки (имя из Designer)
        self.ui.runButton.clicked.connect(self.run)
        self.ui.chooseButton.clicked.connect(self.select_output_dir)

    def run(self):
        url = self.ui.lineEdit.text().strip()

        # 0️⃣ Проверка папки для сохранения сразу
        if not hasattr(self, "output_dir") or not self.output_dir:
            QMessageBox.warning(self, "Ошибка", "Выберите папку для сохранения")
            return

        # 1️⃣ Проверка URL
        if not url:
            QMessageBox.warning(self, "Ошибка", "Empty URL")
            return

        if not is_valid_url(url):
            QMessageBox.warning(self, "Ошибка", "URL not valid\nPut YouTube URL")
            return

        if not video_exists(url):
            QMessageBox.warning(self, "Ошибка", "Video not exist")
            return

        # 2️⃣ Проверка времени
        start_qtime = self.ui.timeEdit.time()
        end_qtime = self.ui.timeEdit_2.time()
        start_sec = (
            start_qtime.hour() * 3600 + start_qtime.minute() * 60 + start_qtime.second()
        )
        end_sec = end_qtime.hour() * 3600 + end_qtime.minute() * 60 + end_qtime.second()

        if start_sec >= end_sec:
            QMessageBox.warning(self, "Ошибка", "Time error")
            return

        # 4️⃣ Скачивание и обрезка аудио
        try:
            # Скачиваем весь аудио файл
            audio_path, video_title = download_audio(url, self.output_dir)

            # Подготавливаем имя конечного MP3
            output_file = self.output_dir / f"{video_title}.mp3"

            # Обрезаем нужный кусок и конвертируем только его в MP3
            cut_path = cut_and_convert_to_mp3(
                audio_path, start_sec, end_sec, output_file
            )

            QMessageBox.information(self, "Готово", f"Файл сохранён:\n{cut_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{e}")

    def select_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.output_dir = Path(folder)
            print(f"Папка выбрана: {self.output_dir}")  # для проверки
