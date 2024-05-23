from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
import sys


class CompaniesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Εταιρείες Παραγωγής")
        self.resize(800, 700)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Κωδικός", "Όνομα", "", ""])

        layout.addWidget(self.table_widget)

        create_user_button = QPushButton("Προσθήκη Νέας εταιρείας")
        create_user_button.setObjectName("create_company")  # Identifier για το UI
        create_user_button.clicked.connect(self.open_create_user)

        layout.addWidget(create_user_button)
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
        self.table_widget.setRowCount(0)

        companies = [
            {"company_code": "S0001", "name": "Company"},
            {"company_code": "S0690", "name": "Kompani"},
            {"company_code": "S0312", "name": "Cob a knee"},
        ]

        for row, company in enumerate(companies):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(company["company_code"])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(company["name"]))

            icon1_button = QPushButton()
            icon1_button.setIcon(QIcon(QPixmap("icons/icon_i.png")))
            icon1_button.setIconSize(QSize(24, 24))
            icon1_button.clicked.connect(lambda _, row=row: self.icon1_clicked(row))
            self.table_widget.setCellWidget(row, 2, icon1_button)

            icon2_button = QPushButton()
            icon2_button.setIcon(QIcon(QPixmap("icons/icon_pen.png")))
            icon2_button.setIconSize(QSize(24, 24))
            icon2_button.clicked.connect(lambda _, row=row, code=company["company_code"]: self.icon2_clicked(row, code))
            self.table_widget.setCellWidget(row, 3, icon2_button)

    def icon1_clicked(self, row):
        print("icon1 clicked")

    def icon2_clicked(self, row, code):
        print(f"Icon2 clicked for company code: {code}")

    def open_create_user(self):
        print("Create user clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load QSS file
    with open("styles/styles_companies.qss", "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)

    window = CompaniesWindow()
    window.show()

    sys.exit(app.exec())
