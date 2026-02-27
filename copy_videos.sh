#!/bin/bash
# Script to copy video files if they exist
if ls city*.mp4 1> /dev/null 2>&1; then
    cp city*.mp4 ./videos/
    echo "Video files copied successfully"
else
    echo "No video files found - skipping"
fi



