import sys
from PyQt6 import QtWidgets
from CurrencyConverter import CurrencyConverterApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec())

#I used this to learn further into JSON: https://www.youtube.com/watch?v=9N6a-VLBa2I&pp=ygUNanNvbiB0dXRvcmlhbA%3D%3D
#I used this to learn how to implement API in my code: https://www.youtube.com/watch?v=bKCORrHbutQ&pp=ygUbaG93IHRvIGltcGxlbWVudCBBUEkgcHl0aG9u
