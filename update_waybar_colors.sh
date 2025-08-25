#!/bin/bash

WAYBAR_FOLDER="$HOME/.config/waybar"
SCSS_FILE="$WAYBAR_FOLDER/style.scss"
CSS_FILE="$WAYBAR_FOLDER/style.css"

# Crea la cartella se non esiste
mkdir -p "$WAYBAR_FOLDER"

# Crea il file solo se non esiste
if [ -e "$SCSS_FILE" ]; then
    echo "Il file scss esiste già"
else
    cat <<'EOF' > "$SCSS_FILE"
@use '../../.cache/wal/colors.scss' as walcolors;

$radius: 15px;
$padding-y: 3px;
$padding-x: 8px;
$margin: 5px;

* {
  border: none;
  border-radius: $radius;
  font-family: "FiraCode Nerd Font";
  font-weight: 500;
  font-size: 14px;
  min-height: 10px;
  transition: all 0.2s ease-in-out;
}

window#waybar {
  background: transparent;
  color: walcolors.$foreground;
}

/* Tooltip */
tooltip {
  background: walcolors.$color0;
  color: walcolors.$color15;
  border-radius: $radius;
  padding: 5px 10px;
}

/* Workspaces */
#workspaces {
  background: walcolors.$background;
  border-radius: $radius;
  margin: $margin;
  padding: 0 $padding-x;
}

#workspaces button {
  padding: 5px 8px;
  margin: 0 4px;
  border-radius: $radius;
  color: walcolors.$color7;
  background: transparent;
}

#workspaces button.active {
  background: walcolors.$color4;
  color: walcolors.$background;
}

#workspaces button.focused {
  background: walcolors.$color6;
  color: walcolors.$background;
}

#workspaces button.urgent {
  background: walcolors.$color1;
  color: walcolors.$background;
}

#workspaces button:hover {
  background: walcolors.$color3;
  color: walcolors.$background;
}

/* Blocchi generali */
#custom-power, #taskbar, #custom-sysupdate, #mpris, #idle_inhibitor,
#cpu, #memory, #disk, #temperature, #battery, #pulseaudio, #network,
#bluetooth, #tray, #backlight, #clock, #custom-notification, #custom-sysinfo {
  background: walcolors.$background;
  padding: $padding-y $padding-x;
  margin: $margin;
  border-radius: $radius;
  color: walcolors.$foreground;
}

/* Modificatori */
#cpu, #memory { color: walcolors.$color2; }
#disk { color: walcolors.$color3; }
#temperature { color: walcolors.$color5; }
#temperature.critical { color: walcolors.$color1; }
#mpris { color: walcolors.$color2; }
#network, #bluetooth { color: walcolors.$color2; }
#pulseaudio { color: walcolors.$color2; }
#pulseaudio.microphone { color: walcolors.$color3; }
#battery { color: walcolors.$color5; }
#backlight { color: walcolors.$color1; }
#custom-power { color: walcolors.$color1; }
#custom-sysupdate.up-to-date { color: walcolors.$color9; }
#custom-sysupdate.updates-available { color: walcolors.$color12; }
#clock { color: walcolors.$color4; }
#custom-sysinfo { color: walcolors.$color4; }

#taskbar button {
  padding: 4px 8px;
  margin: 0 2px;
  border-radius: $radius;
  background: transparent;
  color: walcolors.$color6;
}

#taskbar button.active {
  background: walcolors.$color1;
  color: walcolors.$color4;
  transition: all 0.3s ease-in-out;
}

#taskbar button:hover {
  background: walcolors.$color6;
  color: walcolors.$color5;
  transition: all 0.2s ease-in-out;
}
EOF
fi

# Compila lo SCSS in CSS
sass "$SCSS_FILE" "$CSS_FILE"
sed -i '1{/^@charset "UTF-8";$/d}' $CSS_FILE
