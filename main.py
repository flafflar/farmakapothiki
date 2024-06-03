import sys
from PySide6.QtWidgets import QApplication
from login_form import LoginForm

def main():
    app = QApplication(sys.argv)

    with open("styles/styles.qss") as f:
        qss = f.read()
    app.setStyleSheet(qss)

    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()