##http://127.0.0.1:5000/status/403
##http://127.0.0.1:5000/status?code=200&code=404&code=500
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_statuses():
    status_codes = request.args.getlist('code') 
    results = []

    for code in status_codes:
        try:
            response = requests.get(f'https://httpstatusapi.com/api/v1/{code}')
            data = response.json()
            results.append(data)
        except Exception as e:
            results.append({'code': code, 'error': str(e)})

    return jsonify(results)

@app.route('/status/301', methods=['GET'])
def get_status_301():
    try:
        response = requests.get('https://httpstatusapi.com/api/v1/301')
        data = response.json()
        return jsonify(data), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/403', methods=['GET'])
def get_status_403():
    try:
        response = requests.get('https://httpstatusapi.com/api/v1/403')
        data = response.json()
        return jsonify(data), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
