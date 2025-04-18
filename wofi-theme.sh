#!/bin/bash

# Percorso del file colors.css generato da pywal
colors_file="$HOME/.cache/wal/colors.css"

# Estrai i colori dal file colors.css
background=$(grep -oP '(?<=--background: ).*' "$colors_file")
foreground=$(grep -oP '(?<=--foreground: ).*' "$colors_file")
selected_background=$(grep -oP '(?<=--selected-background: ).*' "$colors_file")
selected_foreground=$(grep -oP '(?<=--selected-foreground: ).*' "$colors_file")
highlight_background=$(grep -oP '(?<=--highlight-background: ).*' "$colors_file")
highlight_foreground=$(grep -oP '(?<=--highlight-foreground: ).*' "$colors_file")

# Crea un file di stile per wofi
cat << EOF > ~/.config/wofi/style.css
/* ~/.config/wofi/style.css */

* {
  background-color: $background;
  color: $foreground;
  font-family: 'Fira Code', monospace;
  font-size: 14px;
  line-height: 1.4;
  margin: 0;
  padding: 0;
  border-radius: 5px;
}

listview {
  background-color: $background;
  color: $foreground;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  padding: 10px;
}

listview.selected {
  background-color: $selected_background;
  color: $selected_foreground;
  border-radius: 5px;
  padding: 10px;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

listview:focus {
  border: 2px solid $highlight_background;
}

scrollbar {
  background-color: rgba(255, 255, 255, 0.3);
  width: 5px;
}

scrollbar:hover {
  background-color: $highlight_background;
  border-radius: 10px;
}

item {
  padding: 8px;
  border-radius: 5px;
  transition: background-color 0.2s, color 0.2s;
}

item:hover {
  background-color: $highlight_background;
  color: $highlight_foreground;
  cursor: pointer;
}
EOF
