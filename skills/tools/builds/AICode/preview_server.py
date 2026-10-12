#!/usr/bin/env python3
"""preview_server.py — repo root static server (0.0.0.0:8000), / -> /output/AICodeVideo.html.

AICodeVideo.html তার asset গুলো relative path-এ খোঁজে (AICodeAudio.mp3, ../src/, ../materials/),
তাই document root হতে হবে repo root — output/ নয়। Browser-side কোনো localhost কল নেই।
"""
import http.server
import os
import socketserver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))  # .../VideoMaking
PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        if self.path in ('/', '', '/index.html'):
            self.send_response(302)
            self.send_header('Location', '/output/AICodeVideo.html')
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    with Server(('0.0.0.0', PORT), Handler) as httpd:
        print(f'serving {ROOT} on 0.0.0.0:{PORT}')
        httpd.serve_forever()
