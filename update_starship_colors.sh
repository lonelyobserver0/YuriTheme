#!/bin/bash

# File di configurazione dei colori generati da pywal
WAL_COLORS="$HOME/.cache/wal/colors.sh"

# File di configurazione di Starship con nomi di variabili colorX
SOURCE_CONFIG="$HOME/.config/starship/starship-conf3.toml"

# File generato con colori sostituiti
OUTPUT_CONFIG="$HOME/.config/starship/starship-pywal.toml"

# Verifica esistenza dei file
if [[ ! -f "$WAL_COLORS" ]]; then
    echo "Errore: $WAL_COLORS non trovato."
    exit 1
fi

if [[ ! -f "$SOURCE_CONFIG" ]]; then
    echo "Errore: $SOURCE_CONFIG non trovato."
    exit 1
fi

# Carica i colori da pywal
source "$WAL_COLORS"

# Copia il file di base in quello di output
cp "$SOURCE_CONFIG" "$OUTPUT_CONFIG"

# Sostituisce ogni colorX con il valore esadecimale corrispondente
for i in {0..15}; do
    varname="color$i"
    colorval="${!varname}"
    if [[ -n "$colorval" ]]; then
        # usa \b per sostituzioni precise, con delimitatori { } per sed
        sed -i "s/\${$varname}/$colorval/g" "$OUTPUT_CONFIG"
    fi
done

echo "Configurazione scritta in: $OUTPUT_CONFIG"
