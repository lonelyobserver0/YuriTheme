#!/bin/bash

# File di configurazione dei colori generati da pywal
WAL_COLORS="$HOME/.cache/wal/colors.sh"

# File di configurazione di Starship
STARSHIP_CONFIG="$HOME/.config/starship/starship-conf3.toml"
BACKUP="$STARSHIP_CONFIG.bak"

# Verifica esistenza dei file
if [[ ! -f "$WAL_COLORS" ]]; then
    echo "Errore: $WAL_COLORS non trovato."
    exit 1
fi

if [[ ! -f "$STARSHIP_CONFIG" ]]; then
    echo "Errore: $STARSHIP_CONFIG non trovato."
    exit 1
fi

# Crea backup
cp "$STARSHIP_CONFIG" "$BACKUP"
echo "Backup creato: $BACKUP"

# Carica i colori da pywal
source "$WAL_COLORS"

# Array di variabili di colore da sostituire
for i in {0..15}; do
    varname="color$i"
    colorval="${!varname}"
    if [[ -n "$colorval" ]]; then
        # Sostituisci "colorX" con "#xxxxxx" nel file TOML
        sed -i "s/\\b$varname\\b/$colorval/g" "$STARSHIP_CONFIG"
    fi
done

echo "Colori aggiornati in $STARSHIP_CONFIG"
