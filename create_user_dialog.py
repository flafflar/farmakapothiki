import sqlite3
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QLineEdit, QMessageBox
from permissions import PermissionsLayout


class CreateUserDialog(QDialog):
    user_created = Signal() # Signal that new year created

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Δημιουργία νέου Χρήστη")

        self.layout = QVBoxLayout()
        self.username_label = QLabel("Όνομα Χρήστη:")
        self.username_lineedit = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_lineedit)

        self.password_label = QLabel("Κωδικός:")
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_lineedit)

        self.fullname_label = QLabel("Ονοματεπώνυμο:")
        self.fullname_lineedit = QLineEdit()
        self.layout.addWidget(self.fullname_label)
        self.layout.addWidget(self.fullname_lineedit)

        self.permissions_layout = PermissionsLayout(0)
        self.layout.addLayout(self.permissions_layout)

        self.create_button = QPushButton("Δημιουργία Χρήστη")
        self.create_button.clicked.connect(self.create_user)
        self.layout.addWidget(self.create_button)

        self.setLayout(self.layout)

    def create_user(self):
     
     username = self.username_lineedit.text()
     password = self.password_lineedit.text()
     fullname = self.fullname_lineedit.text()

     conn = sqlite3.connect("DataBase/DataBase.db") # Connect to the database
     cursor = conn.cursor()

     try:
        #---Insert user data into the database
        cursor.execute("INSERT INTO Users (UserName, Password, FullName) VALUES (?, ?, ?)", (username, password, fullname))
        conn.commit()
        QMessageBox.information(self, "", "Επιτυχής δημιουργία χρήστη!")

        #---Fetch the ID of the newly created user
        cursor.execute("SELECT id FROM Users WHERE UserName = ?", (username,))
        user_id = cursor.fetchone()[0]

        #---Get the permission values
        permissions = [checkbox.isChecked() for checkbox in self.permissions_layout.permission_checkboxes]
        permission_values = tuple(1 if perm else 0 for perm in permissions)

        #---Insert the permissions into the database
        cursor.execute("""
                INSERT INTO Permissions (User_ID, ViewStock, EditStock, AddItem, ViewNotifications, CreateClientList, 
                                         ViewOrders, AddOrders, ChangeOrderState, ViewBills, Invoice, ViewSalaries, UserAdministration) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(user_id,) + permission_values)

        #---Emit the user_created signal
        self.user_created.emit()
        conn.commit()
     except sqlite3.Error as e:
        QMessageBox.warning(self, "Error", f"Αποτυχία δημιουργίας χρήστη: {e}")

     conn.close()
     self.close()


#--- Main to test the dialog
if __name__ == "__main__":
    app = QApplication([])
    dialog = CreateUserDialog()
    dialog.exec()
#---
