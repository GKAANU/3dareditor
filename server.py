#!/usr/bin/env python3
"""
3D AR Material Editor — Local Dev Server
COOP + COEP başlıkları ekleyerek SharedArrayBuffer'ı etkinleştirir.
Bu başlıklar crossOriginIsolated=true yapar, USDZ WebAssembly parser için gereklidir.

Kullanım: python3 server.py
Adres  : http://localhost:8080
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

PORT = 8080

class COIHandler(SimpleHTTPRequestHandler):
    """Tüm yanıtlara Cross-Origin-Opener-Policy ve Cross-Origin-Embedder-Policy ekler."""

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy",  "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Yalnızca HTML/JS/WASM isteklerini logla (favicon, ico vb. gizle)
        path = args[0] if args else ''
        if any(ext in path for ext in ['.html', '.js', '.wasm', '.usdz', '.glb']):
            super().log_message(fmt, *args)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = HTTPServer(("", port), COIHandler)
    print(f"✅  3D AR Editor → http://localhost:{port}")
    print(f"    COOP/COEP başlıkları aktif — SharedArrayBuffer etkin")
    print(f"    Durdurmak için: Ctrl+C\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹  Sunucu durduruldu.")
