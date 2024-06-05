from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QDialog, QLineEdit, QFormLayout, QInputDialog, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
import sys
from database import DatabaseManager, Company

class CompaniesWindow(QWidget):
    """
    Initializes the CompaniesWindow.

    Args:
        db (DatabaseManager): The database manager instance.
    """
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("Εταιρείες Παραγωγής")
        self.resize(782, 700)
        self.setMaximumWidth(782)
        self.setMinimumWidth(782)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Κωδικός", "Όνομα", "", ""])
        self.table_widget.verticalHeader().setVisible(False)

        layout.addWidget(self.table_widget)

        create_company_button = QPushButton("Προσθήκη Νέας εταιρείας")
        create_company_button.setObjectName("create_company")
        create_company_button.clicked.connect(self.open_create_company)

        layout.addWidget(create_company_button)
        layout.setAlignment(Qt.AlignLeft)

        self.setLayout(layout)

        self.load_data()

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

    def load_data(self):
        """
        Loads data from the database and populates the table widget.
        """
        self.table_widget.setRowCount(0)
        companies = self.db.get_all_companies()

        for row, company in enumerate(companies):
            self.table_widget.insertRow(row)
            formatted_code = company.company_code
            displayed_code = f"S{int(formatted_code[1:]):06d}"
            self.table_widget.setItem(row, 0, QTableWidgetItem(displayed_code))
            self.table_widget.setItem(row, 1, QTableWidgetItem(company.name))

            icon1_button = QPushButton()
            icon1_button.setIcon(QIcon(QPixmap("icons/icon_i.png")))
            icon1_button.setObjectName("icon") # identifier for ui
            icon1_button.setIconSize(QSize(24, 24))
            icon1_button.clicked.connect(lambda _, row=row: self.icon1_clicked(row))
            self.table_widget.setCellWidget(row, 2, icon1_button)

            icon2_button = QPushButton()
            icon2_button.setIcon(QIcon(QPixmap("icons/icon_pen.png")))
            icon2_button.setObjectName("icon") # identifier for ui
            icon2_button.setIconSize(QSize(24, 24))
            icon2_button.clicked.connect(lambda _, row=row, code=company.company_code: self.icon2_clicked(row, code))
            self.table_widget.setCellWidget(row, 3, icon2_button)

    def icon1_clicked(self, row):
        """
        Handles the click event for the icon1 button.

        Args:
            row (int): The row index of the clicked button.
        """
        company_code = self.table_widget.item(row, 0).text()[1:]
        company = self.db.get_company(company_code)
        if company:
            QMessageBox.information(self, "Πληροφορίες εταιρείας", f"Κωδικός εταιρείας: S{int(company[0]):04d}\nName: {company[1]}")
        else:
            QMessageBox.warning(self, "Σφάλμα", "Η εταιρεία δεν βρέθηκε")

    def icon2_clicked(self, row, code):
        """
        Handles the click event for the icon2 button.

        Args:
            row (int): The row index of the clicked button.
            code (int): The company code.
        """
        new_name, ok = QInputDialog.getText(self, f"Επεξεργασία εταιρείας", f"Κωδικός: {code}\nΝέο όνομα εταιρείας:")
        if ok:
            company = Company(code, new_name)
            self.db.update_company(company)
            self.load_data()

    def open_create_company(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Προσθήκη Νέας εταιρείας")

        form_layout = QFormLayout()

        company_name_input = QLineEdit()

        form_layout.addRow("Όνομα εταιρείας:", company_name_input)

        create_button = QPushButton("Προσθήκη")
        create_button.clicked.connect(lambda: self.create_company(dialog, company_name_input.text()))

        form_layout.addWidget(create_button)
        dialog.setLayout(form_layout)
        dialog.exec()

    def create_company(self, dialog, company_name):
        """Create a new company in the database.

        Args:
            company_name (str): The name of the company to create.
            dialog (QDialog): The dialog window to close after creating the company.
        """      
        if company_name.strip():  
            existing_companies = self.db.get_all_companies()
            company_code = len(existing_companies) + 1
            company = Company(company_code, company_name)
            self.db.insert_company(company)
            dialog.accept()
            self.load_data()
