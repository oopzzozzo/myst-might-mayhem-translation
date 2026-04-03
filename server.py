#!/usr/bin/env python3
"""Simple server for reader.html — serves /api/books, /api/chapters, /api/chapter plus static files."""
import os, json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))

def is_chinese(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

def list_books():
    return sorted(d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d)) and is_chinese(d))

def list_chapters(book):
    d = os.path.join(BASE, book)
    files = sorted(f for f in os.listdir(d) if f.endswith('.txt'))
    return files

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=BASE, **kw)

    def do_GET(self):
        p = urlparse(self.path)
        qs = parse_qs(p.query)

        if p.path == '/api/books':
            self._json(list_books())
        elif p.path == '/api/chapters':
            book = qs.get('book', [''])[0]
            self._json(list_chapters(book))
        elif p.path == '/api/chapter':
            book = qs.get('book', [''])[0]
            file = qs.get('file', [''])[0]
            path = os.path.join(BASE, book, file)
            if not os.path.realpath(path).startswith(BASE):
                self.send_error(403); return
            try:
                with open(path, encoding='utf-8') as f:
                    self._text(f.read())
            except FileNotFoundError:
                self.send_error(404)
        else:
            super().do_GET()

    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _text(self, text):
        body = text.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # suppress request logs

if __name__ == '__main__':
    port = 8080
    print(f'Serving at http://localhost:{port}/reader.html')
    HTTPServer(('', port), Handler).serve_forever()
