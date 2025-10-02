# #!/bin/bash

APPDIR="$(realpath "$(dirname "$0")")"
DESKTOP_FILE="$HOME/Desktop/Clemens.desktop"

# echo "Installing launcher to your desktop..."

# cat > "$DESKTOP_FILE" <<EOF
# [Desktop Entry]
# Name=Clemens
# Comment=Launch the fullstack app
Exec=$APPDIR/start.sh
Icon=$APPDIR/frontend/public/icon.png

# Type=Application
# Terminal=false
# Categories=Utility;
# EOF

# chmod +x "$DESKTOP_FILE"

# echo "✅ Launcher created on your desktop."
# echo "Double-click it to run the app."

python3 -m venv .env
.env/bin/pip install -r requirements.txt


