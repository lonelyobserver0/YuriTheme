#!/bin/bash

# Percorsi
PYWAL_CSS="$HOME/.cache/wal/colors.css"
OUTPUT="$HOME/.config/stylus/youtube_pywal.user.css"

# Inizio dello userstyle
cat <<EOF > "$OUTPUT"
@-moz-document domain("youtube.com") {
EOF

# Incolla i colori generati da pywal
cat "$PYWAL_CSS" >> "$OUTPUT"

# CSS YouTube custom
cat <<'EOF' >> "$OUTPUT"

    /* Mappatura Pywal → YouTube */
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
EOF
