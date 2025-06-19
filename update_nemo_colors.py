#!/usr/bin/env python3
import json
import os
from pathlib import Path
from hashlib import sha256

WAL_COLORS_PATH = Path.home() / ".cache/wal/colors.json"
GTK_CSS_PATH = Path.home() / ".config/gtk-3.0/gtk.css"

def log(msg, type="info"):
    COLORS = {"info": "\033[1;36m", "ok": "\033[1;32m", "err": "\033[1;31m", "reset": "\033[0m"}
    print(f"{COLORS.get(type, '')}[{type.upper()}] {msg}{COLORS['reset']}")

def read_wal_colors(path):
    if not path.exists():
        log(f"File non trovato: {path}", "err")
        raise FileNotFoundError("Esegui prima 'wal -i <immagine>'")
    with open(path, "r") as f:
        return json.load(f)["colors"]

def generate_gtk_css(colors):
    bg = colors["color0"]
    fg = colors["color7"]
    accent = colors["color4"]

    return f"""\
/* === Tema GTK personalizzato da pywal === */
* {{
    background-color: {bg};
    color: {fg};
    border-color: {accent};
}}

.nemo-window {{
    background-color: {bg};
    color: {fg};
}}

.view {{
    background-color: {bg};
    color: {fg};
}}

.sidebar, .sidebar .view {{
    background-color: {bg};
    color: {fg};
}}

.selected, .selected:focus {{
    background-color: {accent};
    color: {bg};
}}
"""

def write_if_changed(path, content):
    if path.exists():
        current = path.read_text()
        if sha256(current.encode()).hexdigest() == sha256(content.encode()).hexdigest():
            log("Tema già aggiornato, nessuna modifica necessaria.", "info")
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True

def main():
    try:
        colors = read_wal_colors(WAL_COLORS_PATH)
        css = generate_gtk_css(colors)
        if write_if_changed(GTK_CSS_PATH, css):
            log(f"Tema GTK aggiornato: {GTK_CSS_PATH}", "ok")
        else:
            log(f"File GTK invariato: {GTK_CSS_PATH}", "info")
    except Exception as e:
        log(str(e), "err")

if __name__ == "__main__":
    main()
