from PyQt6.QtWidgets import QApplication, QWidget
import sys

# Create an application instance
app = QApplication(sys.argv)

# Create a window
window = QWidget()
window.setWindowTitle("My First PyQt App")
window.resize(400, 300)
window.show()

# Start the event loop
sys.exit(app.exec())