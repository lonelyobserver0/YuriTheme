#!/bin/bash

SWAYNC_FOLDER="$HOME/.config/swaync"

cd $SWAYNC_FOLDER
sass style.scss style.css

swaync-client -rs
