from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from google.cloud import pubsub_v1
import os

# Cloud Pub/Sub settings
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
    exit(1)

publisher = pubsub_v1.PublisherClient()

class PubSubHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            content = data.get('content')
            pubsub_name = data.get('pubsub_name')

            if not content:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Missing "content" field in the request body.'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            if not pubsub_name:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Missing "pubsub_name" field in the request body.'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            topic_path = publisher.topic_path(PROJECT_ID, pubsub_name)

            try:
                publish_future = publisher.publish(topic_path, data=content.encode('utf-8'))
                publish_future.result()  # Block until the publish is complete

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'message': f'Message published to Pub/Sub topic: {pubsub_name}'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                print(f"Error publishing message: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': f'Failed to publish message: {str(e)}'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Invalid JSON format in the request body.'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': f'An unexpected error occurred: {str(e)}'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=PubSubHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Stopping HTTP server.')
        httpd.server_close()

if __name__ == '__main__':
    run()
