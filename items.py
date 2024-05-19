import sys
import sqlite3
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class DatabaseManager:
    def __init__(self, db_name):
        '''
        This method initializes the database manager.
        
        Args:
            db_name: The name of the database file.
            
        Returns:
            None
        '''
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def fetch_all(self):
        '''
        This method fetches all the data from the database.
        
        Args:
            None
            
        Returns:
            list: A list of tuples containing the data.
        '''
        select_query = "SELECT * FROM Products;"
        self.cur.execute(select_query)
        return self.cur.fetchall()

    def fetch_filtered(self, search_text):
        '''
        This method fetches the data from the database that matches the search text, category, and manufacturer.
        
        Args:
            search_text: The text to filter the data by.
            
        Returns:
            list: A list of tuples containing the filtered data.
        '''
        select_query = "SELECT * FROM Products WHERE name LIKE ?"
        params = ['%' + search_text + '%']

        self.cur.execute(select_query, params)
        return self.cur.fetchall()
    
    def fetch_product(self, product_code):
        '''
        This method fetches the product with the given product code.

        Args:
            product_code: The product code of the product.

        Returns:
            list: A list of tuples containing the product data.
        '''
        select_query = "SELECT * FROM Products WHERE product_code = ?;"
        self.cur.execute(select_query, (product_code,))
        return self.cur.fetchall()

    def update_product(self, product_code, name, purchase_cost, selling_price, quantity, quantity_limit):
        '''
        This method updates the product with the given product code.

        Args:
            product_code: The product code of the product.
            name: The name of the product.
            purchase_cost: The purchase cost of the product.
            selling_price: The selling price of the product.
            quantity: The quantity of the product.
            quantity_limit: The quantity limit of the product.

        Returns:
            None
        '''
        update_query = "UPDATE Products SET name = ?, purchase_cost = ?, selling_price = ?, quantity = ?, quantity_limit = ? WHERE product_code = ?;"
        self.cur.execute(update_query, (name, purchase_cost, selling_price, quantity, quantity_limit, product_code))
        self.conn.commit()

    def close(self):
        '''
        This method closes the database connection.

        Args:
            None

        Returns:
            None
        '''
        self.conn.close()

class Ui_MainWindow(object):
    '''
    This class represents the user interface of the main window.

    Methods:
        setupUi: Sets up the user interface of the main window.
        retranslateUi: Retranslates the user interface of the main window.
        update_table: Updates the table with the given data.
    '''
    def setupUi(self, MainWindow):
        '''
        This method sets up the user interface of the main window.
        
        Args:
            MainWindow: The main window of the application.
            
        Returns:
            None
        '''
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QSize(1000, 600))
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.SearchBox = QLineEdit(self.centralwidget)
        self.SearchBox.setObjectName(u"SearchBox")
        self.SearchBox.setMaximumSize(QSize(350, 16777215))
        font = QFont()
        font.setPointSize(12)
        self.SearchBox.setFont(font)

        self.verticalLayout_2.addWidget(self.SearchBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.CategoryBox = QComboBox(self.centralwidget)
        self.CategoryBox.setObjectName(u"CategoryBox")
        self.CategoryBox.setMinimumSize(QSize(220, 0))
        self.CategoryBox.setFont(font)
        self.CategoryBox.addItem("All")
        
        self.verticalLayout_3.addWidget(self.CategoryBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.CompanyBox = QComboBox(self.centralwidget)
        self.CompanyBox.setObjectName(u"CompanyBox")
        self.CompanyBox.setMinimumSize(QSize(220, 0))
        self.CompanyBox.setFont(font)
        self.CompanyBox.addItem("All")

        self.verticalLayout_4.addWidget(self.CompanyBox)

        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setHorizontalHeaderLabels(["Κωδικός", "Όνομα", "Κόστος αγοράς", "Τιμή πώλησης", "Ποσότητα", "Όριο ποσότητας", "", ""])
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalLayout_5.addWidget(self.tableWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        This method retranslates the user interface of the main window.

        Args:
            MainWindow: The main window of the application.

        Returns:
            None
        '''
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03bd\u03b1\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7 \u039f\u03bd\u03cc\u03bc\u03b1\u03c4\u03bf\u03c2:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u039a\u03b1\u03c4\u03b7\u03b3\u03bf\u03c1\u03af\u03b1:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0395\u03c4\u03b1\u03b9\u03c1\u03b5\u03af\u03b1 \u03a0\u03b1\u03c1\u03b1\u03b3\u03c9\u03b3\u03ae\u03c2:", None))

    def update_table_db(self):
        '''
        This method updates the table with the data from the database.

        Args:
            None

        Returns:
            None
        '''
        self.db_manager = DatabaseManager('products.db')
        data = self.db_manager.fetch_all()
        self.update_table(data)
        self.db_manager.close()

    def update_table(self, data):
        '''
        This method updates the table with the given data.

        Args:
            data: A list of tuples containing the data.

        Returns:
            None
        '''
        self.tableWidget.setRowCount(len(data))
        data_coloumns = 6
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data[:data_coloumns]):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
            edit_button = QPushButton("")
            icon = QIcon()
            icon.addFile(u"assets/edit.svg", QSize(), QIcon.Normal, QIcon.Off)
            edit_button.setIcon(icon)
            edit_button.setIconSize(QSize(16, 16))
            product_code = self.tableWidget.item(row_num, 0).text()
            edit_button.clicked.connect(self.edit_item_lambda(product_code))    
            self.tableWidget.setCellWidget(row_num, len(row_data[:data_coloumns]), edit_button)
            info_button = QPushButton("")
            icon1 = QIcon()
            icon1.addFile(u"assets/info.svg", QSize(), QIcon.Normal, QIcon.Off)
            info_button.setIcon(icon1)
            info_button.setIconSize(QSize(16, 16))
            info_button.clicked.connect(self.info_item_lambda(product_code))
            self.tableWidget.setCellWidget(row_num, len(row_data[:data_coloumns]) + 1, info_button)
            # Make the last two columns smaller
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setColumnWidth(len(row_data[:data_coloumns]), 30)
        self.tableWidget.setColumnWidth(len(row_data[:data_coloumns]) + 1, 30)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    
    def edit_item_lambda(self, product_code):
        '''
        This method returns a lambda function that opens the edit window for the given product code.
        
        Args:
            product_code: The product code of the product.
            
        Returns:
            function: A lambda function that opens the edit window.
        '''
        def edit_item():
            print(product_code)
            self.edit_window = ProductWindow(product_code, edit=True, callback=self.update_table_db)
            self.edit_window.show()
        return edit_item
    
    def info_item_lambda(self, product_code):
        '''
        This method returns a lambda function that opens the info window for the given product code.

        Args:
            product_code: The product code of the product.

        Returns:
            function: A lambda function that opens the info window.
        '''
        def info_item():
            print(product_code)
            self.info_window = ProductWindow(product_code, edit=False)
            self.info_window.show()
        return info_item

class ProductWindow(QWidget):
    '''
    This class represents the product window.

    Attributes:
        product_code: The product code of the product.
        edit: A boolean value indicating whether the window is in edit mode.
        callback: A function to call after the window is closed.
        db_manager: The database manager.
        data: The data of the product.

    Methods:
        __init__: Initializes the product window.
        init_ui: Initializes the user interface of the product window.
        save_changes: Saves the changes to the product.
        _close: Closes the window.
    '''
    def __init__(self, product_code, edit=False, callback=None, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.product_code = product_code
        self.edit = edit
        self.db_manager = DatabaseManager('products.db')
        self.data = self.db_manager.fetch_product(product_code)
        self.setWindowTitle("Επεξεργασία Προϊόντος")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        self.product_code_label = QLabel("Κωδικός Προϊόντος:")
        self.product_code_label_value = QLabel(self.product_code)
        if not self.edit:
            self.product_code_label_value.setDisabled(True)
        self.layout.addRow(self.product_code_label, self.product_code_label_value)

        self.name_label = QLabel("Όνομα:")
        self.name_input = QLineEdit()
        self.name_input.setText(self.data[0][1])
        if not self.edit:
            self.name_input.setDisabled(True)
        self.layout.addRow(self.name_label, self.name_input)

        self.purchase_cost_label = QLabel("Κόστος Αγοράς:")
        self.purchase_cost_input = QLineEdit()
        self.purchase_cost_input.setText(str(self.data[0][2]))
        if not self.edit:
            self.purchase_cost_input.setDisabled(True)
        self.layout.addRow(self.purchase_cost_label, self.purchase_cost_input)

        self.selling_price_label = QLabel("Τιμή Πώλησης:")
        self.selling_price_input = QLineEdit()
        self.selling_price_input.setText(str(self.data[0][3]))
        if not self.edit:
            self.selling_price_input.setDisabled(True)
        self.layout.addRow(self.selling_price_label, self.selling_price_input)

        self.quantity_label = QLabel("Ποσότητα:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setText(str(self.data[0][4]))
        if not self.edit:
            self.quantity_input.setDisabled(True)
        self.layout.addRow(self.quantity_label, self.quantity_input)

        self.quantity_limit_label = QLabel("Όριο Ποσότητας:")
        self.quantity_limit_input = QLineEdit()
        self.quantity_limit_input.setText(str(self.data[0][5]))
        if not self.edit:
            self.quantity_limit_input.setDisabled(True)
        self.layout.addRow(self.quantity_limit_label, self.quantity_limit_input)

        self.save_button = QPushButton("Αποθήκευση")
        if not self.edit:
            self.save_button.setDisabled(True)
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button = QPushButton("Ακύρωση")
        self.cancel_button.clicked.connect(self._close)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addRow(button_layout)

    def save_changes(self):
        name = self.name_input.text()
        purchase_cost = self.purchase_cost_input.text()
        selling_price = self.selling_price_input.text()
        quantity = self.quantity_input.text()
        quantity_limit = self.quantity_limit_input.text()
        self.db_manager.update_product(self.product_code, name, purchase_cost, selling_price, quantity, quantity_limit)
        self._close()
    
    def _close(self):
        if self.callback:
            self.callback()
        self.db_manager.close()
        self.close()
class MainWindow(QMainWindow):
    '''
    This class represents the main window of the application.
    
    Attributes:
        ui: The user interface of the main window.
        db_manager: The database manager.
        
    Methods:
        __init__: Initializes the main window.
        load_categories: Loads the categories into the combo box.
        load_manufacturers: Loads the manufacturers into the combo box.
        load_table_data: Loads the initial data into the table.
        filter_table_data: Filters the table data based on the search text, category, and manufacturer.
        closeEvent: Closes the database connection.
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize database manager
        self.db_manager = DatabaseManager('products.db')

        # Load initial data into table
        self.load_table_data()

        # Connect search box and combo box signals to filter method
        self.ui.SearchBox.textChanged.connect(self.filter_table_data)
        self.ui.CategoryBox.currentIndexChanged.connect(self.filter_table_data)
        self.ui.CompanyBox.currentIndexChanged.connect(self.filter_table_data)


    def load_table_data(self):
        data = self.db_manager.fetch_all()
        self.ui.update_table(data)

    def filter_table_data(self):
        search_text = self.ui.SearchBox.text()
        category = self.ui.CategoryBox.currentText()
        manufacturer = self.ui.CompanyBox.currentText()
        filtered_data = self.db_manager.fetch_filtered(search_text)
        self.ui.update_table(filtered_data)

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
