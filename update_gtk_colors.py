#!/usr/bin/env python3
import json
from pathlib import Path

# === Percorsi ===
wal_path = Path.home() / ".cache/wal/colors.json"
gtk2_path = Path.home() / ".gtkrc-2.0"
gtk3_path = Path.home() / ".config/gtk-3.0/gtk.css"
gtk4_path = Path.home() / ".config/gtk-4.0/gtk.css"

# === Template CSS GTK3 & GTK4 ===
def generate_gtk_css_template():
    return """@define-color bg_color   {color0};
@define-color fg_color   {color7};
@define-color accent     {color4};
@define-color highlight  {color2};
@define-color border     {color1};
@define-color hover      {color3};
@define-color warning    {color11};
@define-color error      {color1};
@define-color success    {color10};
@define-color muted      {color5};

* {{
  background-color: @bg_color;
  color: @fg_color;
  border-color: @border;
  border-radius: 6px;
  font-family: "Noto Sans", "Cantarell", sans-serif;
  font-size: 11pt;
}}

window, .background, .nemo-window {{
  background-color: @bg_color;
  color: @fg_color;
}}

headerbar, .titlebar {{
  background-color: shade(@bg_color, 0.95);
  color: @fg_color;
  border-bottom: 1px solid @border;
}}

.sidebar, .places-treeview, .sidebar .view {{
  background-color: shade(@bg_color, 1.03);
  color: @fg_color;
  border-right: 1px solid @border;
}}

.view, treeview, .nemo-desktop, .content-view, columnview, columnview row, list, list row, textview, text {{
  background-color: @bg_color;
  color: @fg_color;
}}

.view:selected, list row:selected, columnview row:selected, treeview:selected, textview:selected {{
  background-color: @highlight;
  color: @bg_color;
}}

.view:hover, treeview:hover, list row:hover, columnview row:hover {{
  background-color: shade(@hover, 1.1);
}}

entry, searchentry, GtkEntry {{
  background-color: shade(@bg_color, 1.05);
  color: @fg_color;
  border: 1px solid @border;
  padding: 4px 6px;
  border-radius: 4px;
}}

entry:focus {{
  border-color: @accent;
}}

button, GtkButton {{
  background-color: shade(@bg_color, 1.1);
  color: @fg_color;
  border: 1px solid @border;
  padding: 6px 10px;
  border-radius: 6px;
}}

button:hover {{
  background-color: @hover;
}}

button:active, button:checked {{
  background-color: @accent;
  color: @bg_color;
}}

button:disabled {{
  background-color: shade(@bg_color, 0.9);
  color: shade(@fg_color, 0.6);
}}

menu, menuitem, popover {{
  background-color: @bg_color;
  color: @fg_color;
  border: 1px solid @border;
}}

menuitem:hover {{
  background-color: @hover;
}}

menuitem:disabled {{
  color: shade(@fg_color, 0.5);
}}

notebook tab {{
  background-color: @bg_color;
  border: 1px solid @border;
  padding: 4px 8px;
}}

notebook tab:active {{
  background-color: @accent;
  color: @bg_color;
}}

check, radio {{
  background-color: shade(@bg_color, 1.05);
  border: 1px solid @border;
}}

check:checked, radio:checked {{
  background-color: @accent;
}}

check:disabled, radio:disabled {{
  background-color: shade(@bg_color, 0.9);
  color: shade(@fg_color, 0.6);
}}

tooltip {{
  background-color: @hover;
  color: @fg_color;
  border: 1px solid @border;
  padding: 4px 8px;
  border-radius: 4px;
}}

scrollbar slider {{
  background-color: @muted;
  border-radius: 4px;
}}

scrollbar slider:hover {{
  background-color: @accent;
}}

progressbar, GtkProgressBar, progressbar trough {{
  background-color: shade(@bg_color, 1.08);
}}

progressbar progress {{
  background-color: @accent;
  border-radius: 6px;
}}

label.link, a {{
  color: @accent;
  text-decoration: underline;
}}

label.link:hover, a:hover {{
  color: shade(@accent, 1.2);
}}

.warning {{ color: @warning; }}
.error   {{ color: @error; }}
.success {{ color: @success; }}
"""

# === Template GTK2 ===
def generate_gtk2_template():
    return """
gtk-color-scheme = "fg_color:{color7},bg_color:{color0},base_color:{color0},text_color:{color7},selected_bg_color:{color2},selected_fg_color:{color0},tooltip_bg_color:{color3},tooltip_fg_color:{color7}"

style "default" {{
  bg[NORMAL]        = "{color0}"
  fg[NORMAL]        = "{color7}"
  base[NORMAL]      = "{color0}"
  text[NORMAL]      = "{color7}"

  bg[SELECTED]      = "{color2}"
  fg[SELECTED]      = "{color0}"
  base[SELECTED]    = "{color2}"
  text[SELECTED]    = "{color0}"

  bg[ACTIVE]        = "{color4}"
  fg[ACTIVE]        = "{color0}"

  bg[INSENSITIVE]   = "{color1}"
  fg[INSENSITIVE]   = "{color5}"

  bg[PRELIGHT]      = "{color3}"
  fg[PRELIGHT]      = "{color7}"
}}

class "GtkWidget" style "default"
"""

# === Carica i colori ===
def load_pywal_colors():
    if not wal_path.exists():
        raise FileNotFoundError("colors.json non trovato. Esegui prima `wal`.")
    with open(wal_path) as f:
        data = json.load(f)
    colors = data["colors"]
    for i in range(16):
        if f"color{i}" not in colors:
            raise KeyError(f"color{i} mancante in colors.json")
    return colors

# === Sostituisci i placeholder ===
def render_template(template: str, colors: dict) -> str:
    return template.format(**colors)

# === Scrive su disco ===
def save_to_file(content: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# === MAIN ===
def main():
    colors = load_pywal_colors()

    gtk_css = render_template(generate_gtk_css_template(), colors)
    gtk2_rc = render_template(generate_gtk2_template(), colors)

    save_to_file(gtk_css, gtk3_path)
    save_to_file(gtk_css, gtk4_path)
    save_to_file(gtk2_rc, gtk2_path)

    print(f"[✓] Temi GTK aggiornati:")
    print(f" - GTK2: {gtk2_path}")
    print(f" - GTK3: {gtk3_path}")
    print(f" - GTK4: {gtk4_path}")

if __name__ == "__main__":
    main()
