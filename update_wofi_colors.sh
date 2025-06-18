#!/bin/bash

# File paths
WAL_JSON="$HOME/.cache/wal/colors.json"
SCSS_TEMPLATE="$HOME/.config/wofi/src/style-template.scss"
SCSS_GENERATED="/tmp/wofi-style-gen.scss"
CSS_OUTPUT="$HOME/.config/wofi/style.css"

# Controlli
if [[ ! -f "$WAL_JSON" || ! -f "$SCSS_TEMPLATE" ]]; then
  echo "❌ File mancante: colors.json o style-template.scss"
  exit 1
fi

# Estrai colori
get_color() {
  jq -r ".colors[\"$1\"]" "$WAL_JSON"
}

bg=$(get_color "color0")
fg=$(get_color "color7")
hl=$(get_color "color4")
sel=$(get_color "color2")

# Genera SCSS con i colori corretti
cat > "$SCSS_GENERATED" <<EOF
\$background: $bg;
\$foreground: $fg;
\$highlight: $hl;
\$selection: $sel;

$(cat "$SCSS_TEMPLATE")
EOF

# Compila in CSS
if ! command -v sass &> /dev/null; then
  echo "❌ Errore: 'sass' non trovato. Installa con: sudo npm install -g sass"
  exit 1
fi

sass "$SCSS_GENERATED" "$CSS_OUTPUT" || {
  echo "❌ Errore nella compilazione SCSS"
  exit 1
}

echo "✅ Tema Wofi generato in: $CSS_OUTPUT"
