import sys
import os
from pathlib import Path

# Automatically re-execute using the project's virtual environment if run with system python
try:
    import uvicorn
    import fastapi
except ImportError:
    script_dir = Path(__file__).resolve().parent
    venv_python = (script_dir.parent.parent / ".venv" / "bin" / "python").absolute()
    if venv_python.exists() and Path(sys.executable).absolute() != venv_python:
        print(f"Required libraries not found in current environment. Re-running server using virtualenv python: {venv_python}")
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        print("Error: Missing required server libraries (uvicorn, fastapi).")
        sys.exit(1)

# pyrefly: ignore [missing-import]
import socket

if __name__ == "__main__":
    import os
    print(f"Pre-checking port 8005... (PID: {os.getpid()})")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', 8005))
        s.close()
        print("Port 8005 is available for binding!")
        import time
        time.sleep(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Port 8005 check failed: {type(e).__name__}: {e}")
        sys.exit(1)
        
    print("Starting uvicorn programmatically...")
    uvicorn.run("main:app", host="127.0.0.1", port=8005, log_level="info")
