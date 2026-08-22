#!/bin/bash
# Double-clickable installer. Finder runs this; it just launches the Python setup.
cd "$(dirname "$0")" || exit 1
python3 install.py
echo ""
echo "Press any key to close..."
read -n 1 -s
