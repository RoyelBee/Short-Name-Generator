import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('D:/Python Code/Short-Name-Generator/icon.png'))

        self.show()

def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(800, 600)
    w.move(400, 200)
    w.setWindowTitle('Short Name Generator')
    e = Example()
    w.show()

    sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()

main()