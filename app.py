from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "application": "python-cicd-ec2"
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello from my automated CI/CD project!")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Application running on port 8000")
    server.serve_forever()
