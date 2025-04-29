# YuriTheme
## Description
 A python app to change popoular linux desktop sofwtare theme according to wallpaper.

## Use
Clone the repository and tell Hyprland to execute the refresh-theme.py at start-up, or create a systemd service 
or whatever your system require.

## Dependencies
pywal, 

## Little advice
Most Linux distro stop you from download python packages and libraries globally, use a service like pipx
(is proved that work whit it) or similar:

`pipx install <package-name>`

and

`pipx inject <library-name> <venv-name>`

## Please note
That for now it works only with swww setted wallpaper.
