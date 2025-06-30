#!/usr/bin/env python3
import json
import os
from pathlib import Path

# === CONFIG ===
theme_name = "WalTheme"
theme_dir = Path.home() / ".themes" / theme_name
wal_colors_path = Path.home() / ".cache" / "wal" / "colors.json"
icon_theme = "Papirus-Dark"
cursor_theme = "Bibata-Modern-Ice"

# Percorsi .config
config_gtk3 = Path.home() / ".config" / "gtk-3.0"
config_gtk4 = Path.home() / ".config" / "gtk-4.0"

def load_pywal_colors():
    with open(wal_colors_path) as f:
        data = json.load(f)
        return data["colors"], data["special"]

def make_dirs():
    for sub in ["gtk-2.0", "gtk-3.0", "gtk-4.0", "metacity-1", "gnome-shell"]:
        (theme_dir / sub).mkdir(parents=True, exist_ok=True)
    config_gtk3.mkdir(parents=True, exist_ok=True)
    config_gtk4.mkdir(parents=True, exist_ok=True)

def write_index_theme():
    content = f"""[Desktop Entry]
Type=X-GNOME-Metatheme
Name={theme_name}
Comment=Pywal-based dynamic theme
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme={theme_name}
MetacityTheme={theme_name}
IconTheme={icon_theme}
CursorTheme={cursor_theme}
"""
    (theme_dir / "index.theme").write_text(content.strip())

def get_gtk2(colors):
    return f"""
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

def get_gtk3_css(colors):
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

def write_settings_ini():
    ini = f"""[Settings]
gtk-theme-name={theme_name}
gtk-icon-theme-name={icon_theme}
gtk-cursor-theme-name={cursor_theme}
gtk-font-name=Sans 10
"""
    (config_gtk3 / "settings.ini").write_text(ini.strip())

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
    (theme_dir / "metacity-1" / "metacity-theme-1.xml").write_text(xml.strip())

def write_files(colors):
    # GTK2
    (theme_dir / "gtk-2.0" / "gtkrc").write_text(get_gtk2(colors).strip())

    # GTK3
    gtk3_css = get_gtk3_css(colors)
    (theme_dir / "gtk-3.0" / "gtk.css").write_text(gtk3_css.strip())
    (config_gtk3 / "gtk.css").write_text(gtk3_css.strip())

    # GTK4
    gtk4_css = get_gtk4_css(colors)
    (theme_dir / "gtk-4.0" / "gtk.css").write_text(gtk4_css.strip())
    (config_gtk4 / "gtk.css").write_text(gtk4_css.strip())

    write_settings_ini()
    write_metacity(colors)
    (theme_dir / "gnome-shell" / "gnome-shell.css").write_text("/* Placeholder */")

def try_apply_theme():
    os.system(f"gsettings set org.gnome.desktop.interface gtk-theme '{theme_name}' || true")
    os.system(f"gsettings set org.gnome.desktop.wm.preferences theme '{theme_name}' || true")
    os.system(f"gsettings set org.gnome.desktop.interface icon-theme '{icon_theme}' || true")
    os.system(f"gsettings set org.gnome.desktop.interface cursor-theme '{cursor_theme}' || true")

def main():
    colors, _ = load_pywal_colors()
    make_dirs()
    write_index_theme()
    write_files(colors)
    try_apply_theme()
    print(f"\n✅ Tema '{theme_name}' generato in '{theme_dir}'.")
    print(f"📁 gtk.css anche in:\n  {config_gtk3}/gtk.css\n  {config_gtk4}/gtk.css")
    print("🎨 Tutti gli stati UI (hover, focus, selezione, disabilitato, tooltip) sono gestiti.")

if __name__ == "__main__":
    main()
