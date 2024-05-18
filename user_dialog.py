from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, Signal
import sqlite3
from permissions import PermissionsLayout

class UserInformationDialog(QDialog):
    user_updated = Signal()

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
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
        self.permissions_layout = PermissionsLayout(self.user_id)
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
        conn = sqlite3.connect("DataBase/DataBase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT UserName, FullName, Password FROM users WHERE ID = ?", (self.user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            username, fullname, password = user_data
            self.username_lineedit.setText(username)
            self.fullname_lineedit.setText(fullname)
            self.password_lineedit.setText(password)
    
        self.permissions_layout.load_permissions() # Load permissions


    #_--Save Button Logic
    def save_clicked(self):
        username = self.username_lineedit.text()
        fullname = self.fullname_lineedit.text()
        password = self.password_lineedit.text()

        # Update the user information in the database
        conn = sqlite3.connect("DataBase/DataBase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET UserName = ?, FullName = ?, Password = ? WHERE ID = ?", (username, fullname, password, self.user_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Επιτυχία", "Τα στοιχεία χρήστη ενημερώθηκαν με επιτυχία.")
        self.user_updated.emit()  # Emit the signal to notify that the user info has been updated
        self.close()
