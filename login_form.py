from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sqlite3
import sys

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()

        #--- Window settings
        self.setWindowTitle("Φόρμα Σύνδεσης")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(100,0,100,100)  #left, top, right, bot
        self.setFixedSize(600, 500)
        self.setObjectName("main_widget")
        self.setWindowIcon(QIcon("icons/Blue_Cross.png"))

        #--- Icon
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("icons/icon_user.png").pixmap(100, 100))
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)
        #---

 #-------Layout Management-------       
        horizontal_layout = QHBoxLayout()

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)
        
        self.username_label = QLabel("Όνομα Χρήστη:")
        self.username_label.setObjectName("username_label")  #Identifier for qss file

        self.username_input = QLineEdit()
        self.username_input.setObjectName("username_input")  #Identifier for qss file
        
        self.password_label = QLabel("Κωδικός:")
        self.password_label.setObjectName("password_label")  #Identifier for qss file

        self.password_input = QLineEdit()
        self.password_input.setObjectName("password_input")  #Identifier for qss file
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Σύνδεση")
        self.login_button.setObjectName("login_button")  #Identifier for qss file

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        layout.addWidget(self.login_button)     

        horizontal_layout.addLayout(layout)
        main_layout.addLayout(horizontal_layout)     
        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.login)

        self.conn = sqlite3.connect("DataBase/DataBase.db")
    
#-------Log In Button Logic-------
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE UserName=? AND Password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self.loginsuccess = True
            cursor.execute("SELECT ID FROM Users WHERE UserName=? AND Password=?", (username, password))
            logedid = cursor.fetchone()
            print ("Login")
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
            self.loginsuccess = False
            print ("Incorrect username or password")


#-------Runs and closes the app-------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the QSS file for UI styles
    with open("styles/styles.qss", "r") as f:
        qss = f.read()
    app.setStyleSheet(qss)

    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec())