import os
import json
import subprocess

def get_colors_from_json():
    colors_path = os.path.abspath(os.path.expanduser("~/.cache/wal/colors.json"))
    with open(colors_path, 'r') as f:
        data = json.load(f)

    colors = data.get("colors", {})
    return {
        "color0": colors.get("color0", "#0C120F"),
        "color1": colors.get("color1", "#305446"),
        "color2": colors.get("color2", "#2C6455"),
        "color3": colors.get("color3", "#346950"),
        "color4": colors.get("color4", "#4E6A53"),
        "color5": colors.get("color5", "#4A9069"),
        "color6": colors.get("color6", "#AC9669"),
        "color7": colors.get("color7", "#c2c3c3"),
        "color8": colors.get("color8", "#586c65"),
        "color9": colors.get("color9", "#305446"),
        "color10": colors.get("color10", "#2C6455"),
        "color11": colors.get("color11", "#346950"),
        "color12": colors.get("color12", "#4E6A53"),
        "color13": colors.get("color13", "#4A9069"),
        "color14": colors.get("color14", "#AC9669"),
        "color15": colors.get("color15", "#c2c3c3"),
    }

def write_style_file():
    colors = get_colors_from_json()
    config_dir = os.path.abspath(os.path.expanduser("~/.config/wofi"))
    os.makedirs(config_dir, exist_ok=True)
    style_path = os.path.join(config_dir, "style.css")

    with open(style_path, 'w') as f:
        f.write(f"""/* ~/.config/wofi/style.css */

window {{
  background-color: {colors['color0']};
  color: {colors['color7']};
  font-family: 'Fira Code', monospace;
  font-size: 16px;
  border-radius: 10px;
}}

#input {{
  background-color: {colors['color1']};
  color: {colors['color7']};
  border: 2px solid {colors['color5']};
  border-radius: 8px;
  padding: 6px;
  margin-bottom: 8px;
  font-size: 16px;
}}

#entry {{
  background-color: {colors['color0']};
  color: {colors['color7']};
  padding: 8px;
  border-radius: 8px;
}}

#entry:selected {{
  background-color: {colors['color5']};
  color: {colors['color0']};
}}

#text {{
  color: {colors['color7']};
}}

#text:selected {{
  color: {colors['color0']};
}}
""")

def apply_theme():
    write_style_file()
    subprocess.run(["wofi", "--show", "drun"])

if __name__ == "__main__":
    apply_theme()
