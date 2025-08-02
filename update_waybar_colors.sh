#!/bin/bash

WAYBAR_FOLDER="$HOME/.config/waybar"
SCSS_FILE="$WAYBAR_FOLDER/style.scss"

sass "$SCSS_FILE" "$WAYBAR_FOLDER/style.css"
