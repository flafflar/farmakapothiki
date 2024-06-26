from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QDialog, QLabel, QMessageBox, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from user_dialog import UserInformationDialog
from create_user_dialog import CreateUserDialog
from database import DatabaseManager
import sys


class AdministrationWindow(QWidget):
    """
    This is a window for user administration.

    Args:
    UserInformationDialog: Custom dialog for displaying user information.
    CreateUserDialog: Custom dialog for creating a new user.

    Returns:
    None.

    Raises:
    None.
    """

    def __init__(self):
        """Initialize the AdministrationWindow."""
        super().__init__()
        #--- Window Settings
        self.setWindowTitle("Λίστα χρηστών")
        self.resize(800, 700)
        #---

        #---Table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Όνομα χρήστη", "Ονοματεπώνυμο", "",""])
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(1, 580) 
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)

        for col in range(2, 4):
            self.table_widget.setColumnWidth(col, 25)
            self.table_widget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
            
        for row in range(self.table_widget.rowCount()):
            for col in range(2): 
                item = self.table_widget.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)
        #---

        #--- Add User Button
        create_user_button = QPushButton("Προσθήκη Νέου Χρήστη")
        create_user_button.setObjectName("create_user")
        create_user_button.clicked.connect(self.open_create_user)
        #---

        #--- Layout Management
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(create_user_button)
        layout.setAlignment(Qt.AlignLeft) 
        self.setLayout(layout)
        #---

        self.db = DatabaseManager()
        self.load_data()


    def load_data(self):
        """Load user data into the table."""
        self.table_widget.setRowCount(0) # Clear the table

        users = self.db.get_all_users() # Fetch user data from database

        # Add user data to the table
        for row, user in enumerate(users):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(user.username)) # Add username to the table
            self.table_widget.setItem(row, 1, QTableWidgetItem(user.full_name)) # Add fullname to the table

            #--- Information Button
            icon1_button = QPushButton()
            icon1_button.setIcon(QIcon(QPixmap("icons/icon_i.png")))
            icon1_button.setIconSize(QSize(24, 24))
            icon1_button.clicked.connect(lambda _, row=row: self.icon_info_clicked(row))
            self.table_widget.setCellWidget(row, 2, icon1_button)

            #--- Edit Button
            icon2_button = QPushButton()
            icon2_button.setIcon(QIcon(QPixmap("icons/icon_pen.png")))
            icon2_button.setIconSize(QSize(24, 24))
            icon2_button.clicked.connect(lambda _, row=row, user=user: self.icon_edit_clicked(row, user))
            self.table_widget.setCellWidget(row, 3, icon2_button)

    def icon_info_clicked(self, row):
        """Show user information dialog when the information icon is clicked."""
        username_item = self.table_widget.item(row, 0)
        fullname_item = self.table_widget.item(row, 1)
        if username_item:
            username = username_item.text()
            fullname = fullname_item.text()
            dialog = QDialog(self)
            dialog.setWindowTitle("Πληροφορίες Χρήστη")
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Όνομα Χρήστη: {username}"))
            layout.addWidget(QLabel(f"Ονοματεπώνυμο: {fullname}"))
            dialog.setLayout(layout)
            dialog.exec()

    def icon_edit_clicked(self, row, user):
        """Open user information dialog for editing when the edit icon is clicked."""
        username = user.username
        password = user.password
        fullname = user.full_name
        user_id = user.id

        dialog = UserInformationDialog(user_id, username)
        dialog.username_lineedit.setText(username)
        dialog.fullname_lineedit.setText(fullname)
        dialog.password_lineedit.setText(password)

        dialog.user_updated.connect(self.load_data)
        dialog.exec()

    def open_create_user(self):
     """Open the dialog for creating a new user."""
     dialog = CreateUserDialog(self) #Open CreateUserDialog
     dialog.user_created.connect(self.load_data) #Reload data
     dialog.exec()

#-------Runs and closes the app-------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the QSS file for UI styles
    with open("styles/adminstyles.qss", "r") as f:
        qss = f.read()
    app.setStyleSheet(qss)

    admin_window = AdministrationWindow()
    admin_window.show()

    sys.exit(app.exec())