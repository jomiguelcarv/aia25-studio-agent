import sys
import requests
from llm_calls import *
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextBrowser, QHBoxLayout
)


class FlaskClientChatUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant")
        self.setGeometry(200, 200, 800, 800)

        # Main layout
        layout = QVBoxLayout()

        # Chat display area
        self.chat_display = QTextBrowser()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input and send button layout
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            self.chat_display.append("<span style='color: red;'>Please enter a message.</span>")
            return

        # Display the user's message in the chat window
        self.chat_display.append(f"<b>You:</b> {message}")
        self.input_field.clear()

        try:
            # Fetch data from Grasshopper
            grasshopper_response = requests.get("http://127.0.0.1:5000/get_from_grasshopper")
            grasshopper_data = grasshopper_response.json()
            print(grasshopper_data)

            # Combine user message with Grasshopper data
            combined_message = f"{message} The Area is {grasshopper_data} m2"

            concept_text = generate_concept(combined_message)

            # Send the concept text to Grasshopper
            response = requests.post(
                "http://127.0.0.1:5000/send_to_grasshopper",
                json={"concept_text": concept_text}
            )
            response_data = response.json()
    
            # Display the server's response in the chat window
            self.chat_display.append(f"<b>Assistant:</b> {response_data}")
        except Exception as e:
            self.chat_display.append("<span style='color: red;'>Error connecting to the server.</span>")
            print(f"Error: {e}")