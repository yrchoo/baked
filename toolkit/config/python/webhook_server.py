from flask import Flask, request, jsonify

try :
    from PySide6.QtCore import Signal
except:
     from PySide2.QtCore import Signal

class WebhookServer():
    NEW_TASK_VERSION = Signal(dict)

    APP = Flask(__name__)

    def __init__(self):

        self._open_server()

    def _open_server(self):
        self.APP.run(host='0.0.0.0', port=5000)

    @APP.route('/webhook', methods=['POST'])
    def webhook(self):
        data = request.json
        print(f"Received data: {data}")
        self.NEW_TASK_VERSION.emit(data)
        return 'OK', 200
