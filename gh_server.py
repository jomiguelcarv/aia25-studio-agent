from flask import Flask, request, jsonify
import sys
import threading
from server.config import *
from llm_calls import *
from ui_pyqt import FlaskClientChatUI  
from PyQt5.QtWidgets import QApplication
app = Flask(__name__)


@app.route('/llm_call', methods=['POST'])
def llm_call():
    data = request.get_json()
    input_string = data.get('input', '')

    answer = classify_input(input_string)

    return jsonify({'response': answer})

stored_data = None
concept_data = None


@app.route('/get_from_grasshopper', methods=['POST', 'GET'])
def get_from_grasshopper():
    global stored_data
    if request.method == 'POST':
        data = request.get_json()
        stored_data = data['input']
    return jsonify(stored_data)

@app.route('/send_to_grasshopper', methods=['POST', 'GET'])
def send_to_grasshopper():
    global concept_data
    
    if request.method == 'POST':
        data = request.get_json()
        concept_data = data['concept_text']
    
    return jsonify(concept_data)



def run_flask():
    app.run(debug=False, use_reloader=False)  # Run Flask server in a separate thread

if __name__ == '__main__':
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start PyQt application
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-size: 14px; }") 
    window = FlaskClientChatUI()
    window.show()
    sys.exit(app.exec_())