#!/bin/bash

# Percorsi
PYWAL_CSS="$HOME/.cache/wal/colors.css"
OUTPUT="$HOME/Code/YuriLand/yuritheme/youtube_pywal.json"

# Inizio contenuto JSON
cat <<EOF > "$OUTPUT"
{
  "name": "YouTube Pywal Theme",
  "enabled": true,
  "updateUrl": null,
  "sections": [
    {
      "name": "YouTube Style",
      "code": "@-moz-document domain('youtube.com') {\n
EOF

# Inserisci i colori, con escaping delle newlines
sed 's/$/\\n/' "$PYWAL_CSS" >> "$OUTPUT"

# Blocca finale CSS (escaped newlines)
cat <<'EOF' >> "$OUTPUT"
\n
    :root {
        --yt-spec-general-background-a: var(--background);
        --yt-spec-general-background-b: var(--color0);
        --yt-spec-general-background-c: var(--color8);
        --yt-spec-brand-background-primary: var(--background);
        --yt-spec-brand-background-secondary: var(--color0);
        --yt-spec-text-primary: var(--foreground);
        --yt-spec-text-secondary: var(--color8);
        --yt-spec-call-to-action: var(--color6);
    }

    body {
        background-color: var(--yt-spec-general-background-a) !important;
        color: var(--yt-spec-text-primary) !important;
    }

    #page-manager,
    ytd-app {
        background-color: var(--yt-spec-general-background-a) !important;
        color: var(--yt-spec-text-primary) !important;
    }

    ytd-video-primary-info-renderer,
    ytd-video-secondary-info-renderer,
    ytd-comments,
    ytd-watch-flexy {
        background-color: var(--yt-spec-general-background-b) !important;
    }

    ytd-thumbnail-overlay-time-status-renderer {
        background-color: var(--color3) !important;
        color: var(--color15) !important;
    }

    a,
    h1, h2, h3,
    .yt-simple-endpoint {
        color: var(--yt-spec-call-to-action) !important;
    }

    ytd-topbar-logo-renderer,
    ytd-masthead {
        background-color: var(--yt-spec-brand-background-primary) !important;
    }

    tp-yt-paper-button,
    ytd-button-renderer {
        background-color: var(--color6) !important;
        color: var(--color0) !important;
    }

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--color8);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background: var(--color0);
    }
}
"
    }
  ]
}
EOF
