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

    def fetch_categories(self):
        '''
        This method fetches all the categories from the database.
        
        Args:
            None
        
        Returns:
            list: A list of categories.
        '''
        select_query = "SELECT DISTINCT category FROM Products;"
        self.cur.execute(select_query)
        return [row[0] for row in self.cur.fetchall()]

    def fetch_manufacturers(self):
        '''
        This method fetches all the manufacturers from the database.

        Args:
            None

        Returns:
            list: A list of manufacturers.
        '''
        select_query = "SELECT DISTINCT manufacturer FROM Products;"
        self.cur.execute(select_query)
        return [row[0] for row in self.cur.fetchall()]

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
        self.tableWidget.setHorizontalHeaderLabels(["Κωδικός", "Όνομα", "Κατηγορία", "Εταιρεία παραγωγής", "Κόστος αγοράς", "Τιμή πώλησης", "Ποσότητα", "Όριο ποσότητας"])
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def update_table(self, data):
        '''
        This method updates the table with the given data.

        Args:
            data: A list of tuples containing the data.

        Returns:
            None
        '''
        self.tableWidget.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
        self.tableWidget.resizeColumnsToContents()

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
        closeEvent: Closes the database connection.
        
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize database manager
        self.db_manager = DatabaseManager('products.db')

        # Load categories and manufacturers into combo boxes
        self.load_categories()
        self.load_manufacturers()

        # Load initial data into table
        self.load_table_data()

    def load_categories(self):
        categories = self.db_manager.fetch_categories()
        self.ui.CategoryBox.addItems(categories)

    def load_manufacturers(self):
        manufacturers = self.db_manager.fetch_manufacturers()
        self.ui.CompanyBox.addItems(manufacturers)

    def load_table_data(self):
        data = self.db_manager.fetch_all()
        self.ui.update_table(data)

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
