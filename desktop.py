"""GATE Prep — native desktop launcher (a pywebview window around the same web app that is published on GitHub Pages)."""
import os
import socket
import threading
import time
import urllib.request

import webview

import server


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class Api:
    """Exposed to the page as window.pywebview.api (full screen button, F11, exit)."""

    def toggle_fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def quit(self):
        webview.windows[0].destroy()


def main():
    server.prepare()
    port = int(os.environ.get("GATEPREP_PORT") or 0) or free_port()   # fixed port only for smoke tests
    threading.Thread(target=lambda: server.app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False), daemon=True).start()
    url = "http://127.0.0.1:%d/" % port
    for _ in range(100):
        try:
            urllib.request.urlopen(url, timeout=0.5)
            break
        except Exception:
            time.sleep(0.1)
    webview.create_window("GATE Prep", url, width=1400, height=900, min_size=(420, 600), background_color="#fbfaf7", js_api=Api())
    webview.start()


if __name__ == "__main__":
    main()
