from GUI import Window
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())