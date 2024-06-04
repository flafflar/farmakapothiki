from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QDialog, QLineEdit, QFormLayout, QPushButton
from PySide6.QtCore import Qt
from database import DatabaseManager, Client

class ClientWindow(QMainWindow):
    def __init__(self, user_id, parent_window):
        super().__init__()
        self.db = DatabaseManager()
        self.user_id = user_id
        self.parent_window = parent_window

        self.setWindowTitle("Λίστα Πελατών")
        self.setGeometry(100, 100, 380, 600)
        self.setMinimumWidth(360)
        self.setMaximumWidth(360)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels([" ", "Ονοματεπώνυμο", "Διεύθυνση", "Τηλέφωνο"])
        self.layout.addWidget(self.table)

        self.table.setColumnWidth(0, 40)

        self.personal_clients = self.db.get_all_personal_clients(self.user_id)
        self.populate_client_table()

        # Button to add new client
        add_client_button = QPushButton("Προσθήκη πελάτη")
        add_client_button.setObjectName("create_client")
        add_client_button.clicked.connect(self.open_add_client)
        self.layout.addWidget(add_client_button, alignment=Qt.AlignLeft)

        # OK button to add selected clients to personal list
        ok_button = QPushButton("OK")
        self.layout.addWidget(ok_button, alignment=Qt.AlignRight)
        ok_button.clicked.connect(self.add_selected_clients_to_personal_list)

    def populate_client_table(self):
        # Clear existing rows
        self.table.setRowCount(0)

        # Fetch all clients from the database
        clients = self.db.get_all_clients()

        # Populate table with client data
        for client in clients:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Add a layout to center the checkbox
            checkbox_layout = QHBoxLayout()
            checkbox_layout.setAlignment(Qt.AlignCenter)

            # Create the checkbox and add it to the layout
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            checkbox_layout.addWidget(checkbox)

            # Create a widget to hold the layout and set it as the cell widget
            checkbox_widget = QWidget()
            checkbox_widget.setLayout(checkbox_layout)
            self.table.setCellWidget(row_position, 0, checkbox_widget)

            self.table.setItem(row_position, 1, QTableWidgetItem(client.fullname))
            self.table.setItem(row_position, 2, QTableWidgetItem(client.address))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(client.phone)))

            # Set client ID as a property of the checkbox widget
            checkbox_widget.setProperty("client_id", client.client_id)

    def open_add_client(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Προσθήκη Πελατών")

        form_layout = QFormLayout()

        client_name = QLineEdit()
        client_address = QLineEdit()
        client_phone = QLineEdit()

        form_layout.addRow("Όνοματεπώνυμο:", client_name)
        form_layout.addRow("Διεύθυνση:", client_address)
        form_layout.addRow("Τηλέφωνο:", client_phone)

        create_button = QPushButton("Προσθήκη")
        create_button.clicked.connect(lambda: self.create_client(dialog, client_name.text(), client_address.text(), client_phone.text()))

        form_layout.addWidget(create_button)
        dialog.setLayout(form_layout)
        dialog.exec()

    def create_client(self, dialog, client_name, client_address, client_phone):
        all_clients = self.db.get_all_clients()
        client_id = len(all_clients) + 1
        client = Client(client_id, fullname=client_name, address=client_address, phone=client_phone)
        self.db.insert_client(client)
        dialog.accept()

        self.populate_client_table()

    def add_selected_clients_to_personal_list(self):
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            checkbox = checkbox_widget.layout().itemAt(0).widget()
            if checkbox.isChecked():
                # Retrieve client ID from the checkbox widget
                client_id = checkbox_widget.property("client_id")
                if client_id is not None:
                    self.db.add_personal_client(self.user_id, client_id)
                else:
                    print("No client ID found")

        self.parent_window.refresh_personal_clients()
        self.close()
