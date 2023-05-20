import sys
from pathlib import Path
import http.server
import socketserver

HERE = Path(__file__).parent
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self) -> None:
    if self.path.endswith('.py'):
      self.render_py()
    else:
      return super().do_GET()

  def render_py(self):
    path = (HERE / self.path[1:]).absolute()
    output = f'{path}, {path.stat().st_size}'.encode('utf8')
    self.send_response(http.HTTPStatus.OK)
    self.send_header("Content-type", "text/html; charset=utf-8")
    self.send_header("Content-Length", len(output))
    self.end_headers()
    self.wfile.write(output)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print("serving at port", PORT)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)
