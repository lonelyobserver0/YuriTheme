#!/bin/bash

WOFI_FOLDER="$HOME/.config/wofi"
SCSS_FILE="$WOFI_FOLDER/style.scss"
CSS_FILE="$WOFI_FOLDER/style.css"

# Assicurati che la directory esista
mkdir -p "$WOFI_FOLDER"

# Crea il file solo se non esiste
if [ -e "$SCSS_FILE" ]; then
    echo "Il file SCSS esiste già: $SCSS_FILE"
else
    echo "Creo il file SCSS: $SCSS_FILE"
    cat <<'EOF' > "$SCSS_FILE"
@use "../../.cache/wal/colors" as walcolors;

* {
  background-color: walcolors.$background;
}

window {
  margin: 0px;
  border: 1px solid walcolors.$background;
  background-color: walcolors.$background;
}

#input {
  margin: 5px;
  border: none;
  color: walcolors.$foreground;
  background-color: walcolors.$background;
}

#inner-box {
  margin: 0px;
  border: none;
  background-color: walcolors.$background;
}

#outer-box {
  margin: 0px;
  border: none;
  background-color: walcolors.$background;
}

#scroll {
  margin: 0px;
  border: none;
}

#text {
  margin: 5px;
  border: none;
  color: walcolors.$foreground;
}

#entry {
  margin: 5px;
}

#entry:selected {
  background-color: walcolors.$background;
}

EOF
fi

# Compila SCSS in CSS
echo "Compilo SCSS in CSS..."
sass "$SCSS_FILE" "$CSS_FILE"
