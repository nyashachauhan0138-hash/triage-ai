import uvicorn
import socket
import sys

if __name__ == "__main__":
    print("Pre-checking port 8000...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', 8000))
        s.close()
        print("Port 8000 is available for binding!")
    except Exception as e:
        print(f"Port 8000 check failed: {e}")
        sys.exit(1)
        
    print("Starting uvicorn programmatically...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
