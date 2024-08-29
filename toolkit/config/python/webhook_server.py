from flask import Flask, request, jsonify

try :
    from PySide6.QtCore import Signal, QObject
except:
     from PySide2.QtCore import Signal, QObject


app = Flask(__name__)

global server
server = None

class WebhookServer(QObject):
    NEW_DATA_OCCUR = Signal(dict)

    def __init__(self):
        super().__init__()
        self.open_server()

    def open_server(self):
        app.run(host='0.0.0.0', port=5000)

    def emit_data(self, data):
        self.NEW_DATA_OCCUR.emit(data)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")
    return data, 200

@app.route('/webhook', methods=['GET'])
def get_tasks():
	return jsonify(webhook)

if __name__ == "__main__":
    server = WebhookServer()
