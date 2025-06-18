import json
import os
from pathlib import Path

# Percorsi
wal_colors_path = Path.home() / ".cache/wal/colors.json"
gtk_css_path = Path.home() / ".config/gtk-3.0/gtk.css"

# Controllo esistenza del file
if not wal_colors_path.exists():
    print("❌ File dei colori non trovato. Esegui prima `wal -i <immagine>`.")
    exit(1)

# Leggi i colori da pywal
with open(wal_colors_path, "r") as f:
    wal_data = json.load(f)

colors = wal_data["colors"]
background = colors["color0"]
foreground = colors["color7"]
accent = colors["color4"]  # ad esempio blu

# Costruzione del tema CSS
gtk_css = f"""
/* pywal + Nemo GTK theme */
* {{
    background-color: {background};
    color: {foreground};
    border-color: {accent};
}}

.nemo-window {{
    background-color: {background};
    color: {foreground};
}}

.view {{
    background-color: {background};
    color: {foreground};
}}

.sidebar, .sidebar .view {{
    background-color: {background};
    color: {foreground};
}}

.selected, .selected:focus {{
    background-color: {accent};
    color: {background};
}}
"""

# Scrittura nel file GTK CSS
os.makedirs(gtk_css_path.parent, exist_ok=True)
with open(gtk_css_path, "w") as f:
    f.write(gtk_css)

print(f"✅ Tema GTK aggiornato con i colori di pywal.")
print(f"👉 Riavvia Nemo o il tuo DE per vedere i cambiamenti.")
