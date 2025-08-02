#!/bin/bash

SWAYNC_FOLDER="$HOME/.config/swaync"
SCSS_FILE="$SWAYNC_FOLDER/style.scss"

if [ -e "$SCSS_FILE" ]; then
    echo "Il file scss esiste già"
else
    cat <<'EOF' > "$SCSS_FILE"
@use '../../.cache/wal/colors.scss' as walcolors;

* {
    outline: none;
    font-family: "Adwaita Sans";
    font-size: 18px;
    text-shadow: none;
    color: walcolors.$foreground;
    background-color: transparent;
    background: transparent;
}

.control-center {
    background-color: rgba(walcolors.$background, 0.8);
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.65);
    padding: 5px;
}

.control-center .notification-row .notification-background {
    border-radius: 15px;
    margin-top: 5px;
}

.notification {
    background-color: rgba(walcolors.$background, 0.8);
}

.notification > *:last-child > * {
    margin: 5px;
}

.summary { font-size: 1.1rem; }
.time { font-size: 0.8rem; }
.body { font-size: 1rem; }

.notification-content {
    padding: 15px 10px 10px 20px;
}

.notification-action > button {
    padding: unset;
    margin: unset;
}
.notification-action > label {
    font-size: 1rem;
    font-weight: normal;
}

.notification.critical {
    background-color: rgba(walcolors.$color1, 0.5);
    box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.65);
}
.notification.low,
.notification.normal {
    background-color: rgba(walcolors.$background, 0.5);
    box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.65);
}

.close-button {
    background-color: rgba(walcolors.$color7, 0.8);
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.35);
}
.close-button:hover {
    background-color: rgba(walcolors.$color1, 0.8);
}

.notification-group-header,
.notification-group-icon {
    font-size: 0.9rem;
}

.notification-group-collapse-button,
.notification-group-close-all-button {
    box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.35);
    background-color: walcolors.$color7;
}

.notification-group-collapse-button:hover {
    background-color: rgba(walcolors.$color4, 0.8);
}
.notification-group-close-all-button:hover {
    background-color: rgba(walcolors.$color1, 0.8);
}

trough highlight {
    background: walcolors.$color4;
}
scale trough {
    margin: 0rem 1rem;
    background-color: walcolors.$color7;
    min-height: 8px;
    min-width: 70px;
}
slider {
    background-color: walcolors.$foreground;
}
tooltip {
    background-color: walcolors.$color7;
}

/*** Widgets ***/
/* Buttons widget */
.widget-buttons-grid {
    font-size: 1rem;
    padding: 20px 20px 10px;
    margin: unset;
}
.widget-buttons-grid > flowbox > flowboxchild > button {
    background: walcolors.$color2;
    box-shadow: 0px 0px 10px rgba(walcolors.$background, 0.8);
    border-radius: 12px;
    min-width: 60px;
    min-height: 30px;
    padding: 6px;
    margin: 0 3px 0;
    transition: all 0.5s ease;
}
.widget-buttons-grid > flowbox > flowboxchild > button:hover {
    background: walcolors.$color4;
}
.widget-buttons-grid > flowbox > flowboxchild > button.toggle:checked {
    background: walcolors.$color4;
}
.widget-buttons-grid > flowbox > flowboxchild > button.toggle:checked:hover {
    background: rgba(walcolors.$color4, 0.8);
}

/* Mpris widget */
$mpris-album-art-overlay: rgba(0, 0, 0, 0.55);
$mpris-button-hover: rgba(0, 0, 0, 0.5);

.widget-mpris .widget-mpris-player {
    padding: 16px;
    margin: 16px 20px;
    background-color: $mpris-album-art-overlay;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.65);
}
.widget-mpris .widget-mpris-player .widget-mpris-album-art {
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.65);
}
.widget-mpris .widget-mpris-player .widget-mpris-title {
    font-weight: bold;
    font-size: 1.2rem;
    margin: 0px 8px 8px 8px;
}
.widget-mpris .widget-mpris-player .widget-mpris-subtitle {
    font-size: 1rem;
}
.widget-mpris .widget-mpris-player > box > button:hover {
    background-color: $mpris-button-hover;
}
.widget-mpris > box > button:hover {
    background: rgba(walcolors.$color4, 0.6);
}

/* Volume widget */
.widget-volume {
    padding: 6px 5px 5px 5px;
    margin: unset;
    font-size: 1.3rem;
}
.widget-volume > box > button {
    border: none;
}
.per-app-volume {
    padding: 4px 8px 8px 8px;
    margin: 0px 8px 8px 8px;
}

/* Backlight widget */
.widget-backlight {
    padding: 0 0 3px 16px;
    margin: unset;
    font-size: 1.1rem;
}

/* DND widget */
.widget-dnd {
    font-weight: bold;
    margin: unset;
    padding: 20px 15px 15px 15px;
}
.widget-dnd > switch {
    font-size: initial;
    border-radius: 100px;
    background: walcolors.$color3;
    border: none;
    box-shadow: none;
    padding: 3px;
}
.widget-dnd > switch:checked {
    background: walcolors.$color2;
}
.widget-dnd > switch slider {
    background: walcolors.$background;
    border-radius: 12px;
    min-width: 18px;
    min-height: 18px;
}

/* Title widget */
.widget-title {
    padding: unset;
    margin: unset;
    font-weight: bold;
    padding: 15px;
}
.widget-title > label {
    font-size: 1.5rem;
}
.widget-title > button {
    padding: unset;
    margin: unset;
    text-shadow: none;
    background: walcolors.$color1;
    border: none;
    box-shadow: none;
    border-radius: 100px;
    padding: 0px 6px;
    transition: all 0.7s ease;
}
.widget-title > button:hover {
    background: rgba(walcolors.$color1, 0.8);
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.65);
}

EOF
fi

sass "$SCSS_FILE" "$SWAYNC_FOLDER/style.css"
swaync-client -rs
