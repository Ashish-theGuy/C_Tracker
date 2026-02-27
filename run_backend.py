"""
Quick script to run the backend server
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory
os.chdir('backend')

# Import and run
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Crowd Detection Backend")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

