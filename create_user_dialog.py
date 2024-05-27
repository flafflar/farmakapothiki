from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QLineEdit, QMessageBox
from permissions import PermissionsLayout
from database import DatabaseManager


class CreateUserDialog(QDialog):
    """Dialog for creating a new user.

        Attributes:
        user_created (Signal): Signal emitted when a new user is created.

        Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """


    user_created = Signal() # Signal that new year created

    def __init__(self, parent=None):
        """Initialize the CreateUserDialog."""

        super().__init__(parent)

        self.db = DatabaseManager()

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
        """Create a new user."""
        username = self.username_lineedit.text()
        password = self.password_lineedit.text()
        fullname = self.fullname_lineedit.text()
     
        try:

            user_id = self.db.add_user(username, password, fullname)

            permissions = [checkbox.isChecked() for checkbox in self.permissions_layout.permission_checkboxes]

            self.db.set_user_permissions(user_id, permissions)

            self.user_created.emit()
            QMessageBox.information(self, "", "Επιτυχής δημιουργία χρήστη!")
        except Exception as e:
            QMessageBox.warning(self, "", "Αποτυχία δημιουργίας χρήστη")

        self.close()


#--- Main to test the dialog
if __name__ == "__main__":
    app = QApplication([])
    dialog = CreateUserDialog()
    dialog.exec()
#---
