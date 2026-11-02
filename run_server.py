"""
run_server.py
=============
MediHybrid Enterprise Production Launcher
Starts the FastAPI application serving both the REST API and the compiled React SPA.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "backend")

# Suppress matplotlib temp cache notices
os.environ["MPLCONFIGDIR"] = os.path.join(backend_dir, ".matplotlib_cache")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
import uvicorn

def main():
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print("=" * 68, flush=True)
    print("  MEDIHYBRID — INTELLIGENT CLINICAL HEALTHCARE SYSTEM", flush=True)
    print("  Soft Computing & Deep Vision Decision Support Platform", flush=True)
    print("=" * 68, flush=True)
    print(f"  * Backend Framework : FastAPI / Python 3.14", flush=True)
    print(f"  * Frontend Web App  : React 18 + Vite + Tailwind CSS", flush=True)
    print(f"  * Module 1 (Hybrid) : DEAP Genetic Algorithm + ANN + Mamdani Fuzzy", flush=True)
    print(f"  * Module 2 (Vision) : Diabetic Retinopathy CNN (APTOS 2019) + Grad-CAM", flush=True)
    print(f"  * Module 3 (AI Bot) : MediBot AI Conversational Health Assistant", flush=True)
    print(f"  * Platform Features : PDF Clinical Report Generator + Algorithm Lab", flush=True)
    print(f"  * Database Engine   : SQLite / SQLAlchemy (medihybrid.db)", flush=True)
    print(f"  * Application URL   : http://localhost:{port}", flush=True)
    print(f"  * Swagger API Docs  : http://localhost:{port}/docs", flush=True)
    print("=" * 68, flush=True)
    print(f"  Server active. Open http://localhost:{port} in your browser.\n", flush=True)

    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
