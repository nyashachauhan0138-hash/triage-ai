# pyrefly: ignore [missing-import]
import uvicorn
import socket
import sys

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
