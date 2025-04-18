import os
import subprocess

def file_exists(path):
    return os.path.exists(os.path.expanduser(path))

subprocess.run(["cp", "-r", os.path.expanduser("~/.cache/wal/colors-rofi.rasi"),
                            os.path.expanduser("~/.config/wofi/style.css")], check=True)