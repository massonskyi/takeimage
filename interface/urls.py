import sys

if sys.platform.startswith('linux'):
    LOCAL_URL = "http://0.0.0.0:8000/"
elif sys.platform.startswith('win'):
    LOCAL_URL = "http://localhost:8000"
