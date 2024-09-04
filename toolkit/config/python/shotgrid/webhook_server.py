from flask import Flask, request, jsonify

import json

from datetime import datetime

app = Flask(__name__)

class WebhookServer():
    def __init__(self):
        self.open_server()

    def open_server(self):
        app.run(host='0.0.0.0', port=5000)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")

    cur_daytime = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    out_path = f"/home/rapa/baked/toolkit/config/python/shotgrid/new_data_json/{cur_daytime}.json"

    with open(out_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return jsonify(data), 200

if __name__ == "__main__":
    server = WebhookServer()


"""
new_data_json에 쌓인 파일들은 crontab으로 하루에 한 번 삭제된다.
"""
