#!/usr/bin/env python3
import json
import os
from pathlib import Path

# === CONFIG ===
theme_name = "WalTheme"
theme_dir = Path.home() / ".themes" / theme_name
wal_colors_path = Path.home() / ".cache" / "wal" / "colors.json"

# Opzionali: icone e cursori
icon_theme = "Papirus-Dark"
cursor_theme = "Bibata-Modern-Ice"

# Percorsi config locali
config_gtk3 = Path.home() / ".config" / "gtk-3.0"
config_gtk4 = Path.home() / ".config" / "gtk-4.0"

# === UTILITY ===

def load_pywal_colors():
    with open(wal_colors_path) as f:
        data = json.load(f)
        return data["colors"], data["special"]

def make_dirs():
    for sub in ["gtk-2.0", "gtk-3.0", "gtk-4.0", "metacity-1", "gnome-shell"]:
        (theme_dir / sub).mkdir(parents=True, exist_ok=True)
    config_gtk3.mkdir(parents=True, exist_ok=True)
    config_gtk4.mkdir(parents=True, exist_ok=True)

# === CSS GENERATORS ===

def get_gtk_css(colors):
    return f"""
@define-color bg_color        {colors['color0']};
@define-color fg_color        {colors['color15']};
@define-color base_color      {colors['color0']};
@define-color text_color      {colors['color7']};

@define-color selected_bg     {colors['color2']};
@define-color selected_fg     {colors['color15']};

@define-color hover_bg        {colors['color4']};
@define-color hover_fg        {colors['color15']};

@define-color disabled_bg     {colors['color8']};
@define-color disabled_fg     {colors['color7']};

@define-color focus_border    {colors['color5']};
@define-color tooltip_bg      {colors['color1']};
@define-color tooltip_fg      {colors['color15']};

* {{
  background-color: @bg_color;
  color: @fg_color;
  border-color: @focus_border;
}}

*:hover {{
  background-color: @hover_bg;
  color: @hover_fg;
}}

*:disabled {{
  background-color: @disabled_bg;
  color: @disabled_fg;
}}

*:selected,
*:focus,
.selection,
:selected {{
  background-color: @selected_bg;
  color: @selected_fg;
}}

tooltip {{
  background-color: @tooltip_bg;
  color: @tooltip_fg;
}}
"""

def get_gtk4_css(colors):
    return f"""
* {{
  background-color: {colors['color0']};
  color: {colors['color15']};
  border-color: {colors['color5']};
}}

*:hover {{
  background-color: {colors['color4']};
  color: {colors['color15']};
}}

*:disabled {{
  background-color: {colors['color8']};
  color: {colors['color7']};
}}

*:selected,
*:focus,
.selection,
:selected {{
  background-color: {colors['color2']};
  color: {colors['color15']};
}}

tooltip {{
  background-color: {colors['color1']};
  color: {colors['color15']};
}}
"""

# === FILE WRITERS ===

def write_index_theme():
    content = f"""[Desktop Entry]
Type=X-GNOME-Metatheme
Name={theme_name}
Comment=Pywal generated GTK theme
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme={theme_name}
MetacityTheme={theme_name}
IconTheme={icon_theme}
CursorTheme={cursor_theme}
"""
    with open(theme_dir / "index.theme", "w") as f:
        f.write(content.strip())

def write_gtk2(colors):
    gtkrc = f"""
style "default" {{
  bg[NORMAL] = "{colors['color0']}"
  fg[NORMAL] = "{colors['color15']}"
  base[NORMAL] = "{colors['color0']}"
  text[NORMAL] = "{colors['color7']}"
  selected_bg[NORMAL] = "{colors['color2']}"
  selected_fg[NORMAL] = "{colors['color15']}"
}}
class "*" style "default"
"""
    with open(theme_dir / "gtk-2.0" / "gtkrc", "w") as f:
        f.write(gtkrc.strip())

def write_gtk3(colors):
    css = get_gtk_css(colors)
    (theme_dir / "gtk-3.0" / "gtk.css").write_text(css.strip())
    (config_gtk3 / "gtk.css").write_text(css.strip())

def write_gtk4(colors):
    css = get_gtk4_css(colors)
    (theme_dir / "gtk-4.0" / "gtk.css").write_text(css.strip())
    (config_gtk4 / "gtk.css").write_text(css.strip())

def write_metacity(colors):
    xml = f"""<metacity_theme>
  <info>
    <name>{theme_name}</name>
    <author>Pywal</author>
  </info>
  <frame_geometry name="normal">
    <distance name="left_width" value="4"/>
    <distance name="right_width" value="4"/>
    <distance name="bottom_height" value="4"/>
    <distance name="title_vertical_pad" value="4"/>
  </frame_geometry>
</metacity_theme>
"""
    with open(theme_dir / "metacity-1" / "metacity-theme-1.xml", "w") as f:
        f.write(xml.strip())

def write_gnome_shell_placeholder():
    (theme_dir / "gnome-shell" / "gnome-shell.css").write_text("/* Placeholder */")

# === APPLY ===

def apply_theme():
    os.system(f"gsettings set org.gnome.desktop.interface gtk-theme '{theme_name}' || true")
    os.system(f"gsettings set org.gnome.desktop.wm.preferences theme '{theme_name}' || true")
    os.system(f"gsettings set org.gnome.desktop.interface icon-theme '{icon_theme}' || true")
    os.system(f"gsettings set org.gnome.desktop.interface cursor-theme '{cursor_theme}' || true")

# === MAIN ===

def main():
    colors, _ = load_pywal_colors()
    make_dirs()
    write_index_theme()
    write_gtk2(colors)
    write_gtk3(colors)
    write_gtk4(colors)
    write_metacity(colors)
    write_gnome_shell_placeholder()
    apply_theme()
    print(f"\n✅ Tema '{theme_name}' creato e applicato.")
    print(f"➡️  File gtk.css scritti anche in:\n  - {config_gtk3}/gtk.css\n  - {config_gtk4}/gtk.css")

if __name__ == "__main__":
    main()
