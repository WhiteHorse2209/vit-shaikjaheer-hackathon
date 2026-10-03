import uvicorn
import webbrowser
import time
from threading import Thread

def start_server():
    print("=" * 70)
    print("S&P Global & CRISIL Campus Hackathon 2026")
    print("AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing")
    print("Candidate: SHAIK JAHEER AHMED | College: VIT Chennai")
    print("=" * 70)
    print("Starting FastAPI Server on http://127.0.0.1:8000 ...")
    print("Dashboard available at: http://127.0.0.1:8000")
    print("Interactive Swagger API docs at: http://127.0.0.1:8000/docs")
    print("=" * 70)
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000")

    Thread(target=open_browser, daemon=True).start()
    start_server()
