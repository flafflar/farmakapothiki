from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, Signal
from permissions import PermissionsLayout
from database import DatabaseManager, User

class UserInformationDialog(QDialog):
    user_updated = Signal()

    def __init__(self, user_id, username, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.username = username

        self.setWindowTitle("Επεξεργασία χρήστη")
        self.setFixedSize(400, 440)
        self.user_id = user_id

        with open("styles/userdstyles.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        # -------------User Data-----------------
        userlayout = QHBoxLayout()
        self.username_label = QLabel("Όνομα χρήστη:")
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_lineedit = QLineEdit()
        self.username_lineedit.setFixedWidth(200) 
        userlayout.addWidget(self.username_label)
        userlayout.addWidget(self.username_lineedit)

        passlayout = QHBoxLayout()
        self.password_label = QLabel("Κωδικός:")
        self.password_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setFixedWidth(200)
        self.password_lineedit.setEchoMode(QLineEdit.Password)
        passlayout.addWidget(self.password_label)
        passlayout.addWidget(self.password_lineedit)

        namelayout = QHBoxLayout()
        self.fullname_label = QLabel("Ονοματεπώνυμο:")
        self.fullname_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.fullname_lineedit = QLineEdit()
        self.fullname_lineedit.setFixedWidth(200) 
        namelayout.addWidget(self.fullname_label)
        namelayout.addWidget(self.fullname_lineedit)

        layout.addLayout(userlayout)
        layout.addLayout(passlayout)
        layout.addLayout(namelayout)

        #---User Permissions
        self.permissions_layout = PermissionsLayout(self.username)
        self.permission_checkboxes = self.permissions_layout.permission_checkboxes

        layout.addLayout(self.permissions_layout)

        #---Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Αποθήκευση")
        self.save_button.clicked.connect(self.save_clicked)
        self.cancel_button = QPushButton("Ακύρωση")

        self.cancel_button.clicked.connect(self.close)  # Close on cancel
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        
        self.load_user_data() #Load user data

    def load_user_data(self):
        user = self.db.get_user_by_username(self.username)
        if user:
            self.username_lineedit.setText(user.username)
            self.fullname_lineedit.setText(user.full_name)
            self.password_lineedit.setText(user.password)

        self.permissions_layout.load_permissions(user.username)


    #---Save Button Logic
    def save_clicked(self):
    # Get username, fullname, and password from the fields
        username = self.username_lineedit.text()
        fullname = self.fullname_lineedit.text()
        password = self.password_lineedit.text()

    # Get permissions from the checkboxes
        permissions = self.permissions_layout.get_permissions()
        user = User(id=self.user_id, username=username, full_name=fullname, password=password, permissions=permissions)
        self.db.update_user(user)

        QMessageBox.information(self, "Επιτυχία", "Τα στοιχεία χρήστη ενημερώθηκαν με επιτυχία.")
        self.user_updated.emit()  # Emit the signal to notify that the user info has been updated
        self.close()