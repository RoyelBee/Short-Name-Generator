import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(800, 600)
    w.move(400, 200)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()

main()