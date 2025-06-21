#!/usr/bin/env python3
import json
import os
from pathlib import Path
from string import Template
import subprocess

# Percorsi
WAL_PATH = Path.home() / ".cache/wal/colors.json"
TEMPLATE_PATH = Path.home() / ".config/wofi/src/style-template.scss"
OUTPUT_SCSS = Path.home() / ".config/wofi/src/wofi.scss"
OUTPUT_CSS = Path.home() / ".config/wofi/style.css"

def load_wal_colors():
    with open(WAL_PATH) as f:
        colors = json.load(f)
    return {
        "BACKGROUND": colors["colors"]["color0"],
        "ON_PRIMARY": colors["colors"]["color15"],
        "PRIMARY": colors["colors"]["color4"],
        "SURFACE": colors["colors"]["color1"],
        "SECONDARY": colors["colors"]["color2"],
        "ON_SURFACE": colors["colors"]["color7"],
        "ON_BACKGROUND": colors["colors"]["color6"],
    }

def generate_scss(template_path, colors):
    with open(template_path) as f:
        template = f.read()
        for key, value in colors.items():
            template = template.replace(key.upper(), value)
        result = template
    OUTPUT_SCSS.write_text(result)
    print("[✓] wofi.scss generato")

def compile_scss():
    try:
        subprocess.run(["sass", str(OUTPUT_SCSS), str(OUTPUT_CSS)], check=True)
        print(f"[✓] Compilato in {OUTPUT_CSS}")
    except FileNotFoundError:
        print("[!] Errore: il comando `sass` non è disponibile. Installa `dart-sass` o `sassc`.")
    except subprocess.CalledProcessError:
        print("[!] Errore durante la compilazione SCSS → CSS.")

def main():
    if not WAL_PATH.exists():
        print("[!] Colori Pywal non trovati. Esegui prima `wal -i <immagine>`.")
        return
    colors = load_wal_colors()
    generate_scss(TEMPLATE_PATH, colors)
    compile_scss()

if __name__ == "__main__":
    main()
