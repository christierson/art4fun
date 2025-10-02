#!/bin/bash

APP_NAME="Clemens"
INSTALL_PATH="/Applications/$APP_NAME"
DESKTOP_PATH="$HOME/Desktop"
LAUNCHER_NAME="$APP_NAME Launcher.command"
ICON_NAME="$APP_NAME.icns"  # Optional, if you have a .icns icon file

echo "🛠 Installing $APP_NAME to $INSTALL_PATH..."

# 1. Install app to /Applications
mkdir -p "$INSTALL_PATH"
cp -r . "$INSTALL_PATH"

# 2. Create a terminal launcher for CLI use
echo "#!/bin/bash" > /usr/local/bin/$APP_NAME
echo "\"$INSTALL_PATH/$APP_NAME\"" >> /usr/local/bin/$APP_NAME
chmod +x /usr/local/bin/$APP_NAME
echo "✅ CLI launcher installed as '$APP_NAME'"

# 3. Create a desktop launcher
echo "#!/bin/bash" > "$DESKTOP_PATH/$LAUNCHER_NAME"
echo "\"$INSTALL_PATH/$APP_NAME\"" >> "$DESKTOP_PATH/$LAUNCHER_NAME"
chmod +x "$DESKTOP_PATH/$LAUNCHER_NAME"
echo "✅ Desktop launcher created: $LAUNCHER_NAME"

# 4. Set icon (optional)
if [ -f "$INSTALL_PATH/$ICON_NAME" ]; then
    # Use AppleScript to assign icon to the .command file
    /usr/bin/osascript <<EOF
    tell application "Finder"
        set iconFile to POSIX file "$INSTALL_PATH/$ICON_NAME" as alias
        set targetFile to POSIX file "$DESKTOP_PATH/$LAUNCHER_NAME" as alias
        set the icon of targetFile to iconFile
    end tell
EOF
    echo "🎨 Icon applied to desktop launcher."
else
    echo "ℹ️ No icon found ($ICON_NAME), skipping icon assignment."
fi

echo "✅ $APP_NAME has been installed successfully!"