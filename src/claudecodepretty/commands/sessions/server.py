import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class SessionHandler(BaseHTTPRequestHandler):
    html_content = ""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._serve_html(self.html_content)
        elif parsed.path == "/api/session":
            params = parse_qs(parsed.query)
            file_path = params.get("file", [None])[0]
            if not file_path or not os.path.exists(file_path):
                self._serve_error(404, "Session file not found")
                return
            from claudecodepretty.renderers.session import parse_session_to_html

            html = parse_session_to_html(file_path)
            self._serve_html(html)
        else:
            self._serve_error(404, "Not found")

    def _serve_html(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _serve_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def log_message(self, format, *args):
        pass


def serve_session(file_path, port=7860):
    from claudecodepretty.renderers.session import parse_session_to_html

    html = parse_session_to_html(file_path)

    handler = type("Handler", (SessionHandler,), {"html_content": html})
    try:
        server = HTTPServer(("localhost", port), handler)
    except OSError:
        print(f"Error: port {port} already in use. Try --port <number>")
        return 1

    url = f"http://localhost:{port}"
    print(f"Serving session at {url}")
    print("Press Ctrl+C to stop")
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer stopped")

    return 0
