from yt_dlp import YoutubeDL


def is_valid_url(url: str) -> bool:
    return url.startswith("https://www.youtube.com/") or url.startswith(
        "https://youtu.be/"
    )


def video_exists(url: str) -> bool:
    try:
        with YoutubeDL({"quiet": True}) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False
