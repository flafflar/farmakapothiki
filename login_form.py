from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QMessageBox
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QIcon, QRegularExpressionValidator
import sys
from database import DatabaseManager
from main_window import MainWindow

class LoginForm(QWidget):
    """A class for a login form widget.

    Attributes:
        username_label (QLabel): A label for the username input field.
        username_input (QLineEdit): A line edit field for entering the username.
        password_label (QLabel): A label for the password input field.
        password_input (QLineEdit): A line edit field for entering the password.
        login_button (QPushButton): A button to trigger the login action.
    """
    def __init__(self):
        """Initialize the LoginForm widget."""
        super().__init__()

        #--- Window settings
        self.setWindowTitle("Φόρμα Σύνδεσης")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(100,0,100,100)  #left, top, right, bot
        self.setFixedSize(600, 500)
        self.setObjectName("main_widget")
        self.setWindowIcon(QIcon("icons/Blue_Cross.png"))

        # Create and apply the validator for the username input field
        regex = QRegularExpression(r"\S+")  # Match anything that is not whitespace
        validator = QRegularExpressionValidator(regex)
        self.username_input = QLineEdit()
        self.username_input.setObjectName("username_input")
        self.username_input.setValidator(validator)

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
        self.db = DatabaseManager()
    
#-------Log In Button Logic-------
    def login(self):
        """Login logic when the login button is clicked."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = self.db.get_user_by_username(username)

        if user and user.password == password:
            self.loginsuccess = True
            self.open_main_window(username)
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
            QMessageBox.warning(self, "Σφάλμα", "Λάθος όνομα χρήστη ή κωδικός.")
            self.loginsuccess = False

    def open_main_window(self, username):
        """Open the main window and close the login form."""
        self.main_window = MainWindow(username)
        with open("styles/mainwindowstyles.qss", "r") as f:
            self.main_window.setStyleSheet(f.read())
        self.main_window.show()
        self.close()


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