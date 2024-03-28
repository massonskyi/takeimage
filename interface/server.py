# server.py
import threading

from server.app import app

server_started_event = threading.Event()


def run_server():
    print("Starting server...")
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    server_started_event.set()
    server.run()
