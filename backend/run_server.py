# pyrefly: ignore [missing-import]
import uvicorn
import socket
import sys

if __name__ == "__main__":
    import os
    print(f"Pre-checking port 8001... (PID: {os.getpid()})")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', 8001))
        s.close()
        print("Port 8001 is available for binding!")
    except Exception as e:
        print(f"Port 8001 check failed: {type(e).__name__}: {e}")
        sys.exit(1)
        
    print("Starting uvicorn programmatically...")
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info")
