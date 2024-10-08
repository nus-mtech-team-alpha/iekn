from flask import Flask, jsonify
import consul
import socket
import signal
import sys

app = Flask(__name__)
local_ip = socket.gethostbyname(socket.gethostname())

def register_service_with_consul():
    client = consul.Consul(host='consul', port=8500)
    client.agent.service.register(
        name='rag-service',
        service_id='rag-service-1',
        address=local_ip,
        tags=['flask', 'python', 'api'],
        port=5000,
        check={
            'http': f'http://{local_ip}:5000/health',
            'interval': '5s',
            'timeout': '10s'
        }
    )

@app.route('/health', methods=['GET'])
def hello_world():
    return jsonify(message="OK")

def deregister_service_from_consul():
    client = consul.Consul(host='consul', port=8500)
    client.agent.service.deregister('rag-service-1')

def handle_shutdown_signal(signum, frame):
    print("Shutting down...")
    deregister_service_from_consul()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, handle_shutdown_signal)
signal.signal(signal.SIGTERM, handle_shutdown_signal)

if __name__ == '__main__':
    register_service_with_consul()
    app.run(host=local_ip, port=5000)