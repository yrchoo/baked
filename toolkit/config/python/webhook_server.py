from flask import Flask, request, jsonify

try :
    from PySide6.QtCore import Signal, QObject
except:
     from PySide2.QtCore import Signal, QObject

class WebhookServer(QObject):
    NEW_DATA_OCCUR = Signal(dict)

    APP = Flask(__name__)

    def __init__(self):
        super().__init__()
        # self._open_server()

    def open_server(self):
        self.APP.run(host='0.0.0.0', port=5000)

    @APP.route('/webhook', methods=['POST'])
    def webhook():
        data = request.json
        print(f"Received data: {data}")
        # NEW_DATA_OCCUR.emit(data)
        return 'OK', 200


if __name__ == "__main__":
    WebhookServer()
