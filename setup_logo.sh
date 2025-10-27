#!/bin/bash
# Koenig Logo Setup Script for Mac

echo "🎨 Koenig Logo Setup for Followup Reminder App"
echo "=============================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create assets directory
echo "📁 Creating assets directory..."
mkdir -p assets

# Check if logo exists in Downloads
DOWNLOADS_LOGO="$HOME/Downloads/followup_reminder_app/assets/koenig_logo.png"
TARGET_LOGO="./assets/koenig_logo.png"

if [ -f "$DOWNLOADS_LOGO" ]; then
    echo "✅ Found logo in Downloads folder"
    echo "📋 Copying logo to assets folder..."
    cp "$DOWNLOADS_LOGO" "$TARGET_LOGO"
    
    if [ -f "$TARGET_LOGO" ]; then
        echo "✅ Logo copied successfully!"
        echo ""
        echo "Logo location: $TARGET_LOGO"
        ls -lh "$TARGET_LOGO"
    else
        echo "❌ Error: Failed to copy logo"
        exit 1
    fi
else
    echo "❌ Logo not found at: $DOWNLOADS_LOGO"
    echo ""
    echo "Please do one of the following:"
    echo "1. Copy your logo to: $SCRIPT_DIR/assets/koenig_logo.png"
    echo "2. Or provide the path to your logo file:"
    echo ""
    read -p "Enter full path to your logo file (or press Enter to skip): " CUSTOM_LOGO
    
    if [ -n "$CUSTOM_LOGO" ] && [ -f "$CUSTOM_LOGO" ]; then
        echo "📋 Copying logo..."
        cp "$CUSTOM_LOGO" "$TARGET_LOGO"
        if [ -f "$TARGET_LOGO" ]; then
            echo "✅ Logo copied successfully!"
        else
            echo "❌ Error: Failed to copy logo"
            exit 1
        fi
    else
        echo "⚠️  Skipping logo setup"
        echo "You can manually copy your logo to: $TARGET_LOGO"
        exit 0
    fi
fi

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Run the app: streamlit run app.py"
echo "2. Logo will appear on login page and sidebar"
echo ""
echo "To customize logo display, see: LOGO_SETUP.md"
echo "=============================================="
