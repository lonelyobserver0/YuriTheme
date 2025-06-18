#!/bin/bash

# File di output
OUTPUT="$HOME/.cache/wal/rofi-wal-theme.rasi"
WAL_COLORS="$HOME/.cache/wal/colors-rofi-dark.rasi"

# Scrivi il tema combinato
cat > "$OUTPUT" <<EOF
/* === Colori generati da pywal === */
$(cat "$WAL_COLORS")

/* === Configurazione Rofi === */
configuration {
  show-icons: true;
  icon-theme: "Papirus";
}

* {
  font: "Noto Sans 11";
  border-radius: 16;
  spacing: 10;
}

window {
  padding: 24;
  border: 2;
  border-radius: 16;
  background-color: @background;
}

mainbox {
  children: [inputbar, listview];
  spacing: 12;
}

inputbar {
  padding: 8 12;
  border-radius: 12;
  background-color: @background;
}

entry {
  expand: false;
  width: 50%;
  placeholder: "Cerca applicazioni…";
  text-color: @foreground;
}

listview {
  columns: 1;
  lines: 8;
  spacing: 8;
  fixed-height: false;
  scrollbar: true;
  border-radius: 12;
}

element {
  padding: 8 12;
  border-radius: 12;
  background-color: transparent;
  text-color: @foreground;
}

element-icon {
  size: 48;
  margin: 0 16 0 0;
  border-radius: 8;
}

element selected {
  background-color: @color2;
  text-color: @background;
}

element active {
  background-color: @color4;
  text-color: @background;
}
EOF

echo "Tema Rofi generato in: $OUTPUT"
