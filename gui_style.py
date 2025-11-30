GLOBAL_STYLES = """
QWidget {
    background-color: #f5f5f5;
    font-family: Segoe UI;
    font-size: 16px;
}

QPushButton[class="blue"] {
    background-color: #1E88E5;
    color: white;
    border-radius: 12px;
    padding: 12px;
}
QPushButton[class="blue"]:hover {
    background-color: #1565C0;
}

QPushButton[class="green"] {
    background-color: #43A047;
    color: white;
    border-radius: 12px;
    padding: 12px;
}
QPushButton[class="green"]:hover {
    background-color: #2E7D32;
}

QPushButton[class="red"] {
    background-color: #E53935;
    color: white;
    border-radius: 12px;
    padding: 12px;
}
QPushButton[class="red"]:hover {
    background-color: #C62828;
}

#statusLabel[status="ok"] {
    color: #008800;
    font-weight: bold;
}
#statusLabel[status="bad"] {
    color: #cc0000;
    font-weight: bold;
}

QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    color: #000000;
    font-size: 15px;
}

QMessageBox QPushButton {
    background-color: #007AFF;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    min-width: 70px;
    font-weight: 500;
}

QMessageBox QPushButton:hover {
    background-color: #0A84FF;
}
"""

button_class_blue = "blue"
button_class_green = "green"
button_class_red = "red"
