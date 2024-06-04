from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QSizePolicy, QPushButton, QTableWidgetItem
from PySide6.QtCore import Qt
from database import DatabaseManager
from clients_list import ClientWindow

class PersonalClientsWindow(QWidget):
    """Initialize the ClientsWindow.

    Args:
       db (DatabaseManager): The database manager instance.
       user_id (int): The ID of the currently logged-in user.
    """
    def __init__(self, username):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("Προσωπικό πελατολόγιο")
        self.resize(900, 700)
        self.user_id = self.db.get_user_by_username(username).id

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Ονοματεπώνυμο", "Διεύθυνση", "Τηλέφωνο"])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.table_widget.setColumnWidth(0, 400)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(2, 300)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)

        self.open_client_button = QPushButton("Προσθήκη πελατών")
        self.open_client_button.clicked.connect(self.open_all_clients_window)
        layout.addWidget(self.open_client_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.populate_client_table()

    def populate_client_table(self):
        # Clear existing rows
        self.table_widget.setRowCount(0)

        # Fetch personal clients for the current user from the database
        personal_clients = self.db.get_all_personal_clients(self.user_id)

        if personal_clients:
            # Populate table with client data
            for client in personal_clients:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                self.table_widget.setItem(row_position, 0, QTableWidgetItem(client.fullname))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(client.address))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(client.phone)))
        else:
            print("No personal clients found for the logged-in user.")


    def open_all_clients_window(self):
        """Open the ClientWindow."""
        self.client_window = ClientWindow(self.user_id, self)
        with open("styles/styles_clients.qss", "r") as f:
            self.client_window.setStyleSheet(f.read())  
        self.client_window.show()

    def refresh_personal_clients(self):
        """Refresh the personal clients list."""
        self.populate_client_table()
