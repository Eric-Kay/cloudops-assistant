import os
import time


def version_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    timestamp = int(time.time())
    return f"{name}_v{timestamp}{ext}"