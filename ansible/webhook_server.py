

from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        subprocess.call(["/home/ubuntu/ansible/run_playbook.sh"])
        return 'OK', 200
    return 'OK', 200  # For GET requests, return 200 OK

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

