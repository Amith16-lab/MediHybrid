import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, "..", "backend")
if os.path.exists(backend_path):
    sys.path.insert(0, os.path.abspath(backend_path))

from app.main import app
