"""
Backward-compatible entrypoint: run the Flask app when invoked as
`python backend/run_backend.py` so startup scripts that reference that
path don't fail.
"""
import os

from app import app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    print("=" * 60)
    print("Running backend from backend/run_backend.py")
    print("=" * 60)
    app.run(debug=debug, host='0.0.0.0', port=port)
