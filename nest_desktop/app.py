import http.server
import socketserver
import os
import sys

NEST_DESKTOP_HOST = os.environ.get("NEST_DESKTOP_HOST", "127.0.0.1")
NEST_DESKTOP_PORT = os.environ.get("NEST_DESKTOP_PORT", 54286)


def run(host=NEST_DESKTOP_HOST, port=NEST_DESKTOP_PORT):
    "Start a simple http server to hand out the app."
    if len(sys.argv) > 1:
        host = sys.argv[1]
        port = int(sys.argv[2])

    web_dir = os.path.join(os.path.dirname(__file__), "app")
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((host, port), Handler) as httpd:
        httpd.serve_forever()
