import sys

from PyQt5.QtWidgets import QApplication

from src.gui.app_gui import AppGUI
from src.gui.pyqt5_gui import PyQt5GUI

if __name__ == '__main__':
    # app = AppGUI()
    # app.mainloop()
    app = QApplication(sys.argv)

    window = PyQt5GUI()
    window.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
