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
    return f"""\
@define-color bg_color   {colors["color0"]};
@define-color fg_color   {colors["color7"]};
@define-color accent     {colors["color4"]};
@define-color select     {colors["color2"]};
@define-color border     {colors["color1"]};
@define-color hover      {colors["color3"]};

/* === Tema GTK 3 per Nemo (generato da pywal) === */

* {{
  background-color: @bg_color;
  color: @fg_color;
  border-color: @border;
  transition: background-color 150ms ease, color 150ms ease;
  border-radius: 6px;
}}

.nemo-window, window {{
  background-color: @bg_color;
  color: @fg_color;
}}

.sidebar,
.sidebar .view,
.places-treeview {{
  background-color: shade(@bg_color, 1.05);
  color: @fg_color;
  border-right: 1px solid @border;
  padding: 4px;
}}

.view,
.nemo-desktop,
.content-view,
.nemo-list-view,
treeview {{
  background-color: @bg_color;
  color: @fg_color;
  border: none;
  padding: 6px;
  font-size: 11pt;
}}

.view:hover row,
treeview:hover row {{
  background-color: @hover;
  color: @fg_color;
}}

.selected,
:selected,
treeview:selected,
.view:selected,
row:selected {{
  background-color: @select;
  color: @bg_color;
}}

.selected:focus,
row:selected:focus {{
  background-color: @accent;
  color: @bg_color;
}}

.entry,
.search-bar,
entry {{
  background-color: shade(@bg_color, 1.08);
  color: @fg_color;
  border: 1px solid @border;
  border-radius: 4px;
  padding: 4px 6px;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
}}

.header-bar,
.titlebar {{
  background-color: shade(@bg_color, 0.97);
  color: @fg_color;
  border-bottom: 1px solid @border;
  padding: 6px;
}}

tooltip {{
  background-color: @hover;
  color: @fg_color;
  border-radius: 4px;
  padding: 4px 8px;
  border: 1px solid @border;
}}

progressbar {{
  background-color: shade(@bg_color, 1.1);
  border-radius: 6px;
  border: 1px solid @border;
}}

progressbar trough,
progressbar progress {{
  background-color: @accent;
  border-radius: 6px;
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
