import sys
from PyQt5 import QtWidgets
from main import main

if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)
    window = main()
    window.show() 
    sys.exit(app.exec_()) 
    