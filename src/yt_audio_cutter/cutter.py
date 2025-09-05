import os
from pathlib import Path

from pydub import AudioSegment
from pydub.utils import which


def cut_and_convert_to_mp3(
    input_file: Path, start_sec: float, end_sec: float, output_file: Path
) -> Path:
    # Проверка наличия ffmpeg
    if which("ffmpeg") is None:
        raise RuntimeError("FFmpeg не найден. Установите ffmpeg и добавьте его в PATH")

    # Загружаем исходный аудио файл (например m4a)
    audio = AudioSegment.from_file(input_file)

    start_ms = int(start_sec * 1000)
    end_ms = int(end_sec * 1000)

    if end_ms > len(audio):
        end_ms = len(audio)

    # Обрезаем нужный кусок
    segment = audio[start_ms:end_ms]

    # Экспортируем уже только этот кусок в MP3
    segment.export(output_file, format="mp3")

    # Удаляем полный исходный аудиофайл
    os.remove(input_file)

    return output_file
