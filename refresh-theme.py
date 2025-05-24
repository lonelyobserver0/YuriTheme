import os
import subprocess
import time
import inotify.adapters
import wofitheme
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.cache/theme_changer_errors.log")


def log_error(message, error):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}: {error}\n")
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


def run_if_exists(path):
    path = os.path.expanduser(path)
    if os.path.exists(path) and os.access(path, os.X_OK):
        try:
            subprocess.run([path], check=True)
        except subprocess.CalledProcessError as e:
            log_error(f"Errore nell'esecuzione di {path}", e)


def apply_terminal_themes():
    if command_exists("kitty") and file_exists("~/.cache/wal/colors-kitty.conf"):
        try:
            subprocess.run(["kitty", "@", "set-colors", "-a", os.path.expanduser("~/.cache/wal/colors-kitty.conf")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a kitty", e)

    if command_exists("fish") and file_exists("~/.cache/wal/colors.fish"):
        try:
            subprocess.run(["fish", "-c", "source ~/.cache/wal/colors.fish"], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a fish", e)

    if command_exists("alacritty") and file_exists("~/.cache/wal/colors-alacritty.yml"):
        try:
            subprocess.run(["alacritty", "--config-file", os.path.expanduser("~/.cache/wal/colors-alacritty.yml")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema ad Alacritty", e)


def apply_desktop_themes():
    try:
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", "FlatColor"], check=True)
    except subprocess.CalledProcessError as e:
        log_error("Errore nell'applicare il tema GTK", e)

    os.environ["QT_STYLE_OVERRIDE"] = "kvantum"

    if file_exists("~/.cache/wal/colors-firefox.css"):
        firefox_profile = os.path.expanduser("~/.mozilla/firefox/*.default-release/chrome/")
        try:
            subprocess.run(["cp", "-r", os.path.expanduser("~/.cache/wal/colors-firefox.css"), firefox_profile], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Firefox", e)

    if file_exists("~/.cache/wal/colors.json"):
        try:
            # wofitheme.apply_theme()
            pass
        except Exception as e:
            log_error("Errore nell'applicare il tema a Wofi", e)


def apply_bar_themes():
    run_if_exists("~/Code/YuriLand/YuriTheme/css-to-scss-waybar.sh")
    run_if_exists("~/Code/YuriLand/YuriTheme/css-to-scss-swaync.sh")
    run_if_exists("~/Code/YuriLand/YuriTheme/make-rofi-theme.sh")

    if file_exists("~/.cache/wal/colors-foot.ini"):
        try:
            subprocess.run(["cp", os.path.expanduser("~/.cache/wal/colors-foot.ini"), os.path.expanduser("~/.config/foot/")], check=True)
        except subprocess.CalledProcessError as e:
            log_error("Errore nell'applicare il tema a Foot", e)


def reload_bars():
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


def update_starship_colors():
    run_if_exists("~/Code/YuriLand/YuriTheme/update_starship_colors.sh")


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

    apply_desktop_themes()
    apply_terminal_themes()
    apply_bar_themes()
    update_starship_colors()
    reload_bars()

    print("Tema aggiornato!")
    print("Monitoraggio delle modifiche dello sfondo...")


def main():
    swww_cache = os.path.expanduser("~/.cache/swww/eDP-1")
    if not os.path.exists(swww_cache):
        log_error("Errore", "Il file di cache di swww non esiste. Assicurati che swww sia in esecuzione.")
        return

    if "--once" in os.sys.argv:
        apply_theme()
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
