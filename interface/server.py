# server.py
import threading
import sys
from server.app import app

server_started_event = threading.Event()


def run_server():
    print("Starting server...")
    import uvicorn
    config = None
    if sys.platform.startswith('linux'):
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    elif sys.platform.startswith('win'):
        config = uvicorn.Config(app, host="localhost", port=8000)
    if config is None:
        raise "Not avaible on your platform"
    server = uvicorn.Server(config)

    server_started_event.set()
    server.run()
