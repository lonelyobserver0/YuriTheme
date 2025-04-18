#!/bin/bash

WAYBAR_FOLDER="$HOME/.config/waybar"

INPUT_FILE="$HOME/.cache/wal/colors-waybar.css"
OUTPUT_FILE="$WAYBAR_FOLDER/src/walcolors.scss"

# Inizializza il file di output
echo "" > "$OUTPUT_FILE"

# Leggi il file di input riga per riga
while IFS= read -r line; do
    # Controlla se la riga inizia con @define-color
    if [[ $line == @define-color* ]]; then
        # Estrai il nome della variabile e il valore
        var_name=$(echo "$line" | sed -E 's/@define-color ([^ ]+) (.*);/\$\1: \2;/')
        # Scrivi la variabile nel file di output
        echo "$var_name" >> "$OUTPUT_FILE"
    fi
done < "$INPUT_FILE"

sass "$WAYBAR_FOLDER/src/main.scss" "$WAYBAR_FOLDER/style.css"
