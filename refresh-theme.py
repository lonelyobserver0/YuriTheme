import os
import subprocess
import time
import inotify.adapters
import wofitheme

def log_error(message, error):
    with open(os.path.expanduser("~/.cache/theme_changer_errors.log"), "a") as log_file:
        log_file.write(f"{message}: {error}\n")
    print(f"{message}: {error}")


def get_wallpaper():
    try:
        swww_cache = os.path.expanduser("~/.cache/swww/eDP-1")
        if os.path.exists(swww_cache):
            with open(swww_cache, "r") as f:
                return f.read().strip()
        else:
            log_error("Errore", "Il file ~/.cache/swww/eDP-1 non esiste.")
            return None
    except Exception as e:
        log_error("Errore nell'ottenere lo sfondo da swww", e)
        return None


def file_exists(path):
    return os.path.exists(os.path.expanduser(path))


def command_exists(command):
    return subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def apply_theme():
    wallpaper = get_wallpaper()
    if not wallpaper:
        print("Impossibile ottenere lo sfondo.")
        return

    print(f"Generando il tema da: {wallpaper}")
    try:
        subprocess.run(["wal", "-i", wallpaper], check=True)
    except subprocess.CalledProcessError as e:
        log_error("Errore nell'applicare il tema con pywal", e)
        return

    try:
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", "FlatColor"], check=True)
    except subprocess.CalledProcessError as e:
        log_error("Errore nell'applicare il tema GTK", e)

    os.environ["QT_STYLE_OVERRIDE"] = "kvantum"

    if command_exists("kitty") and file_exists("~/.cache/wal/colors-kitty.conf"):
        try:
            subprocess.run(["kitty", "@", "set-colors", "-a", os.path.expanduser("~/.cache/wal/colors-kitty.conf")],
                           check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a kitty", e)

    if command_exists("fish") and file_exists("~/.cache/wal/colors.fish"):
        try:
            subprocess.run(["fish", "-c", "source ~/.cache/wal/colors.fish"], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a fish", e)

    if command_exists("alacritty") and file_exists("~/.cache/wal/colors-alacritty.yml"):
        try:
            subprocess.run(["alacritty", "--config-file", os.path.expanduser("~/.cache/wal/colors-alacritty.yml")],
                           check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema ad Alacritty", e)

    firefox_profile = os.path.expanduser("~/.mozilla/firefox/*.default-release/chrome/")
    if file_exists("~/.cache/wal/colors-firefox.css"):
        try:
            subprocess.run(["cp", "-r", os.path.expanduser("~/.cache/wal/colors-firefox.css"), firefox_profile],
                           check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Firefox", e)

    if file_exists("~/.cache/wal/colors.json"):
        try:
            #wofitheme.apply_theme()
            pass
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Wofi", e)

    if file_exists("~/.cache/wal/colors-waybar.css"):
        try:
            subprocess.run([os.path.expanduser("~/Code/YuriLand/YuriTheme/css-to-scss-waybar.sh")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Waybar", e)

    if file_exists("~/.cache/wal/colors-foot.ini"):
        try:
            subprocess.run(["cp", os.path.expanduser("~/.cache/wal/colors-foot.ini"), os.path.expanduser("~/.config/foot/")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Foot", e)

    if file_exists("~/.cache/wal/colors-waybar.css"):
        try:
            subprocess.run([os.path.expanduser("~/Code/YuriLand/YuriTheme/css-to-scss-swaync.sh")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a SwayNC", e)

    if file_exists("~/.cache/wal/colors-rofi-dark.rasi"):
        try:
            subprocess.run([os.path.expanduser("~/Code/YuriLand/YuriTheme/make-rofi-theme.sh")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Rofi", e)

    if command_exists("pkill"):
        try:
            subprocess.run(["pkill", "-USR1", "ironbar"], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nel ricaricare Ironbar", e)

        try:
            subprocess.run(["pkill", "-USR1", "waybar"], check=True)
            subprocess.run(['zsh', '-c', "bgp waybar"], capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nel ricaricare Waybar", e)

    print("Tema aggiornato!")
    print("Monitoraggio delle modifiche dello sfondo...")


def main():
    swww_cache = os.path.expanduser("~/.cache/swww/eDP-1")
    if not os.path.exists(swww_cache):
        log_error("Errore", "Il file di cache di swww non esiste. Assicurati che swww sia in esecuzione.")
        return

    try:
        inotify_instance = inotify.adapters.Inotify()
        inotify_instance.add_watch(swww_cache)
    except Exception as e:
        log_error("Errore nell'inizializzazione di inotify", e)
        return

    print("Monitoraggio delle modifiche dello sfondo avviato...")
    for event in inotify_instance.event_gen(yield_nones=False):
        (_, type_names, _, _) = event
        if "IN_MODIFY" in type_names:
            apply_theme()


if __name__ == "__main__":
    main()
