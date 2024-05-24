from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QApplication, QMessageBox, QDialog, QLineEdit, QFormLayout, QInputDialog
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
import sys
from database import DatabaseManager

class categoriesWindow(QWidget):
    """
    Initializes the CategoriesWindow.

    Args:
        db (DatabaseManager): The database manager instance.
    """
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Κατηγορίες")
        self.resize(782, 700)
        self.setMaximumWidth(782)
        self.setMinimumWidth(782)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Κωδικός", "Όνομα", "", ""])
        self.table_widget.verticalHeader().setVisible(False)

        layout.addWidget(self.table_widget)

        create_category_button = QPushButton("Προσθήκη Νέας κατηγορίας")
        create_category_button.setObjectName("create_category")
        create_category_button.clicked.connect(self.open_create_category)

        layout.addWidget(create_category_button)
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
        categories = self.db.get_all_categories()

        for row, category in enumerate(categories):
            self.table_widget.insertRow(row)
            formatted_code = f"S{int(category[0]):04d}"
            self.table_widget.setItem(row, 0, QTableWidgetItem(formatted_code))
            self.table_widget.setItem(row, 1, QTableWidgetItem(category[1]))

            icon1_button = QPushButton()
            icon1_button.setIcon(QIcon(QPixmap("icons/icon_i.png")))
            icon1_button.setObjectName("icon") #identifier for ui
            icon1_button.setIconSize(QSize(24, 24))
            icon1_button.clicked.connect(lambda _, row=row: self.icon1_clicked(row))
            self.table_widget.setCellWidget(row, 2, icon1_button)

            icon2_button = QPushButton()
            icon2_button.setIcon(QIcon(QPixmap("icons/icon_pen.png")))
            icon2_button.setObjectName("icon") #identifier for ui
            icon2_button.setIconSize(QSize(24, 24))
            icon2_button.clicked.connect(lambda _, row=row, code=category[0]: self.icon2_clicked(row, code))
            self.table_widget.setCellWidget(row, 3, icon2_button)

    def icon1_clicked(self, row):
        """
        Handles the click event for the icon1 button.

        Args:
            row (int): The row index of the clicked button.
        """
        categoryCode = self.table_widget.item(row, 0).text()[1:]  # Remove the 'C' prefix
        category = self.db.get_category(categoryCode)
        if category:
            QMessageBox.information(self, "Πληροφορίες κατηγορίας", f"Κωδικός κατηγορίας: C{int(category[0]):04d}\nName: {category[1]}")
        else:
            QMessageBox.warning(self, "Error", "Η εταιρεία δεν βρέθηκε")

    def icon2_clicked(self, row, code):
        """
        Handles the click event for the icon2 button.

        Args:
            row (int): The row index of the clicked button.
            code (int): The category code.
        """
        new_name, ok = QInputDialog.getText(self, f"Επεξεργασία κατηγορίας", f"Κωδικός: C{int(code):04d}\nΝέο όνομα κατηγορίας:", text=self.db.get_category(code)[1])
        if ok:
            self.db.update_category(code, new_name)
            self.load_data()

    def open_create_category(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Προσθήκη Νέας κατηγορίας")


        form_layout = QFormLayout()

        category_name_input = QLineEdit()

        form_layout.addRow("Όνομα κατηγορίας:", category_name_input)

        create_button = QPushButton("Προσθήκη")
        create_button.clicked.connect(lambda: self.create_category(dialog, category_name_input.text()))

        form_layout.addWidget(create_button)
        dialog.setLayout(form_layout)
        dialog.exec()

    def create_category(self, dialog, category_name):
        categoryCode = self.db.get_next_category_code()
        self.db.insert_category(categoryCode, category_name)
        dialog.accept()
        self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseManager("database.db")

    app.setWindowIcon(QIcon("icons/Blue_Cross.png"))
    with open("styles/styles_categories.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = categoriesWindow(db)
    window.show()
    sys.exit(app.exec())
