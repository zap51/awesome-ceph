from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    # Handle POST requests
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Print received data
        print("Received POST request:")
        print(post_data.decode('utf-8'))

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Received POST request".encode('utf-8'))

# Main function
def main():
    # Set up HTTP server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    # Start HTTP server
    httpd.serve_forever()

if __name__ == '__main__':
    main()
