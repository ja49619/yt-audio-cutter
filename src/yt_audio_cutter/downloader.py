from pathlib import Path

from yt_dlp import YoutubeDL


def download_audio(youtube_url: str, output_dir: Path) -> tuple[Path, str]:
    from yt_dlp import YoutubeDL

    output_path = output_dir / "%(title)s.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_path),
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        audio_file = Path(filename).with_suffix(".m4a")
        video_title = info.get("title", "output")
    return audio_file, video_title
