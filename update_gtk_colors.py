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
    return """
@define-color background   {color0};
@define-color foreground   {color7};
@define-color primary      {color4};
@define-color secondary    {color3};
@define-color success      {color10};
@define-color warning      {color11};
@define-color error        {color1};
@define-color border       {color5};

* {{
  font-family: "Noto Sans", sans-serif;
  font-size: 11pt;
  color: @foreground;
  background-color: @background;
  border-color: @border;
  transition: all 100ms ease-in-out;
}}

window, .background, .nemo-window {{
  background-color: @background;
  color: @foreground;
}}

headerbar, .titlebar {{
  background-color: shade(@background, 0.95);
  color: @foreground;
  border-bottom: 1px solid @border;
}}

button, .button {{
  background-color: shade(@background, 1.05);
  border: 1px solid @border;
  padding: 6px 12px;
  border-radius: 4px;
}}
button:hover, .button:hover {{
  background-color: @secondary;
}}
button:active, .button:checked {{
  background-color: @primary;
  color: @background;
}}
button:disabled {{
  background-color: shade(@background, 0.9);
  color: shade(@foreground, 0.6);
}}

entry, textview, searchentry, GtkEntry {{
  background-color: shade(@background, 1.02);
  color: @foreground;
  border: 1px solid @border;
  border-radius: 4px;
  padding: 4px;
}}
entry:focus {{
  border-color: @primary;
}}

*:selected, treeview:selected, list:selected, row:selected {{
  background-color: @primary;
  color: @background;
}}

list:hover, row:hover, treeview:hover, columnview row:hover {{
  background-color: shade(@secondary, 1.1);
}}

menu, menuitem, popover, .menu {{
  background-color: @background;
  color: @foreground;
  border: 1px solid @border;
}}
menuitem:hover {{
  background-color: @secondary;
}}
menuitem:disabled {{
  color: shade(@foreground, 0.5);
}}

notebook tab {{
  background-color: @background;
  border: 1px solid @border;
  padding: 4px 8px;
}}
notebook tab:active {{
  background-color: @primary;
  color: @background;
}}

check, radio {{
  background-color: shade(@background, 1.05);
  border: 1px solid @border;
}}
check:checked, radio:checked {{
  background-color: @primary;
}}
check:disabled, radio:disabled {{
  background-color: shade(@background, 0.9);
  color: shade(@foreground, 0.6);
}}

scrollbar slider {{
  background-color: @border;
  border-radius: 4px;
}}
scrollbar slider:hover {{
  background-color: @primary;
}}

tooltip {{
  background-color: @secondary;
  color: @foreground;
  border: 1px solid @border;
  padding: 4px 8px;
  border-radius: 4px;
}}

label.link, a {{
  color: @primary;
  text-decoration: underline;
}}
label.link:hover, a:hover {{
  color: shade(@primary, 1.2);
}}

.warning {{ color: @warning; }}
.error   {{ color: @error; }}
.success {{ color: @success; }}
"""

# === Template GTK2 ===
def generate_gtk2_template():
    return """
gtk-color-scheme = "fg_color:{color7},bg_color:{color0},base_color:{color0},text_color:{color7},selected_bg_color:{color4},selected_fg_color:{color0},tooltip_bg_color:{color3},tooltip_fg_color:{color7}"

style "default" {{
  bg[NORMAL]        = "{color0}"
  fg[NORMAL]        = "{color7}"
  base[NORMAL]      = "{color0}"
  text[NORMAL]      = "{color7}"

  bg[SELECTED]      = "{color4}"
  fg[SELECTED]      = "{color0}"

  bg[ACTIVE]        = "{color3}"
  fg[ACTIVE]        = "{color7}"

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
    print("[✓] Temi GTK aggiornati:")
    print(f" - GTK2: {gtk2_path}")
    print(f" - GTK3: {gtk3_path}")
    print(f" - GTK4: {gtk4_path}")

if __name__ == "__main__":
    main()
