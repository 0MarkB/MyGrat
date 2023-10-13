import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(800, 800, 880, 800)
window.move(60, 15)

window.show()

sys.exit(app.exec_())