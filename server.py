from flask import Flask, jsonify, json
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/run_script')
def run_script():
    result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
    if result.returncode == 0:
        with open('result.json') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Script failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
