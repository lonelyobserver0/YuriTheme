#!/bin/bash

WOFI_FOLDER="$HOME/.config/wofi"
SCSS_FILE="$HOME/style.scss"

if [ -e "$SCSS_FILE" ]; then
    echo "Il file scss esiste già"
else
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

cd ~/.config/wofi/
sass "$SCSS_FILE" "$WOFI_FOLDER/style.css"
