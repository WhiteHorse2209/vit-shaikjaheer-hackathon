import uvicorn
import webbrowser
import time
import socket
import sys
from threading import Thread

def wait_for_server(host="127.0.0.1", port=8000, timeout=15):
    """Waits until the server port is open before launching browser."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.5)
    return False

def launch_browser():
    if wait_for_server():
        time.sleep(0.5)
        webbrowser.open("http://127.0.0.1:8000")

def start_server():
    print("=" * 70)
    print("  S&P Global & CRISIL Campus Hackathon 2026")
    print("  AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing")
    print("  Candidate: SHAIK JAHEER AHMED | College: VIT Chennai")
    print("=" * 70)
    print("  Starting FastAPI Server on http://127.0.0.1:8000 ...")
    print("  Dashboard UI:    http://127.0.0.1:8000")
    print("  Swagger Docs:    http://127.0.0.1:8000/docs")
    print("  (Press CTRL+C anytime to stop the server)")
    print("=" * 70)

    # Launch browser in a background thread only once port 8000 is accepting connections
    Thread(target=launch_browser, daemon=True).start()

    try:
        uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped gracefully by user.")
        sys.exit(0)

if __name__ == "__main__":
    start_server()
