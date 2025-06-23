#!/usr/bin/env python3
import json
from pathlib import Path

# === Percorsi ===
wal_path = Path.home() / ".cache/wal/colors.json"
gtk2_path = Path.home() / ".gtkrc-2.0"
gtk3_path = Path.home() / ".config/gtk-3.0/gtk.css"
gtk4_path = Path.home() / ".config/gtk-4.0/gtk.css"

# === Template CSS comune (GTK3 + GTK4) ===
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

/* Stile base */
* {{
  background-color: @bg_color;
  color: @fg_color;
  border-color: @border;
  font-family: "Noto Sans", "Cantarell", sans-serif;
  font-size: 11pt;
  transition: all 100ms ease-in-out;
  border-radius: 6px;
}}

window, .nemo-window, .background {{
  background-color: @bg_color;
  color: @fg_color;
}}

.header-bar,
.titlebar,
.header-bar.default-decoration,
headerbar {{
  background-color: shade(@bg_color, 0.95);
  color: @fg_color;
  border-bottom: 1px solid @border;
}}

.sidebar,
.places-treeview,
.sidebar .view {{
  background-color: shade(@bg_color, 1.03);
  color: @fg_color;
  border-right: 1px solid @border;
}}

.view,
treeview,
.nemo-desktop,
.content-view,
columnview,
columnview row,
list,
list row,
textview,
text {{
  background-color: @bg_color;
  color: @fg_color;
}}

.view:selected,
treeview:selected,
list row:selected,
columnview row:selected,
textview:selected {{
  background-color: @highlight;
  color: @bg_color;
}}

.view:hover,
treeview:hover,
list row:hover,
columnview row:hover {{
  background-color: @hover;
}}

entry,
GtkEntry,
.search-bar,
searchentry,
searchbar {{
  background-color: shade(@bg_color, 1.08);
  color: @fg_color;
  border: 1px solid @border;
  padding: 4px 6px;
  border-radius: 4px;
}}

button,
GtkButton {{
  background-color: shade(@bg_color, 1.1);
  color: @fg_color;
  border: 1px solid @border;
  padding: 6px 10px;
}}

button:hover {{
  background-color: @hover;
}}

button:active,
button:checked {{
  background-color: @accent;
  color: @bg_color;
}}

scrollbar {{
  background-color: transparent;
}}

scrollbar slider {{
  background-color: @muted;
  border-radius: 4px;
}}

scrollbar slider:hover {{
  background-color: @accent;
}}

tooltip {{
  background-color: @hover;
  color: @fg_color;
  border-radius: 4px;
  padding: 4px 8px;
  border: 1px solid @border;
}}

progressbar,
GtkProgressBar,
progressbar trough {{
  background-color: shade(@bg_color, 1.08);
}}

progressbar progress {{
  background-color: @accent;
  border-radius: 6px;
}}

label.link,
a {{
  color: @accent;
  text-decoration: underline;
}}

label.link:hover,
a:hover {{
  color: shade(@accent, 1.2);
}}

.warning {{ color: @warning; }}
.error   {{ color: @error; }}
.success {{ color: @success; }}
"""

# === Template per GTK2 ===
def generate_gtk2_template():
    return """
gtk-color-scheme = "base_color:{color0},fg_color:{color7},bg_color:{color0},text_color:{color7},selected_bg_color:{color2},selected_fg_color:{color0},tooltip_bg_color:{color3},tooltip_fg_color:{color7}"

style "default" {{
  bg[NORMAL]        = "{color0}"
  fg[NORMAL]        = "{color7}"
  base[NORMAL]      = "{color0}"
  text[NORMAL]      = "{color7}"
  bg[SELECTED]      = "{color2}"
  fg[SELECTED]      = "{color0}"
  base[SELECTED]    = "{color2}"
  text[SELECTED]    = "{color0}"
}}

class "GtkWidget" style "default"
"""

# === Carica colori da pywal ===
def load_pywal_colors():
    if not wal_path.exists():
        raise FileNotFoundError("File colors.json non trovato. Esegui prima `wal`.")
    with open(wal_path) as f:
        data = json.load(f)
    colors = data["colors"]
    # Validazione base
    for i in range(16):
        if f"color{i}" not in colors:
            raise KeyError(f"Manca il colore color{i} in colors.json")
    return colors

# === Sostituisci nel template ===
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
    
    # GTK 3 & 4
    gtk_css = render_template(generate_gtk_css_template(), colors)
    save_to_file(gtk_css, gtk3_path)
    save_to_file(gtk_css, gtk4_path)

    # GTK 2
    gtk2_rc = render_template(generate_gtk2_template(), colors)
    save_to_file(gtk2_rc, gtk2_path)

    print(f"[✓] Temi aggiornati:")
    print(f"  - GTK2:  {gtk2_path}")
    print(f"  - GTK3:  {gtk3_path}")
    print(f"  - GTK4:  {gtk4_path}")

if __name__ == "__main__":
    main()
