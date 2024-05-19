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

    def get_new_product_code(self):
        '''
        This method returns a new product code.

        Args:
            None

        Returns:
            product_code: The new product code
        '''
        self.cur.execute('SELECT MAX(product_code) FROM products')
        result = self.cur.fetchone()
        if result[0] is None:
            return "P000001"
        else:
            result = int(result[0][1:]) + 1
            return "P" + str(result).zfill(6)
        
    def insert_product(self, product_code, name, type, cost, sell_price, quantity, quantity_limit):
        '''
        This method inserts a new product to the database.

        Args:
            product_code: The product code
            name: The name of the product
            type: The type of the product
            cost: The cost of the product
            sell_price: The selling price of the product
            quantity: The quantity of the product
            quantity_limit: The quantity limit of the product

        Returns:
            None
        '''
        self.cur.execute('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)', (product_code, name, cost, sell_price, quantity, quantity_limit, type))
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
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(80, 16777215))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.db_manager = DatabaseManager('products.db')
        self.horizontalLayout.addWidget(self.label)

        self.product_code_label = QLabel(self.centralwidget)
        self.product_code_label.setObjectName(u"product_code_label")
        self.product_code_label.setFont(font)

        self.horizontalLayout.addWidget(self.product_code_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.nameLine = QLineEdit(self.centralwidget)
        self.nameLine.setObjectName(u"nameLine")

        self.verticalLayout_2.addWidget(self.nameLine)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.TypeCombo = QComboBox(self.centralwidget)
        self.TypeCombo.setObjectName(u"TypeCombo")
        self.TypeCombo.addItem("Φάρμακο")
        self.TypeCombo.addItem("Προϊόν")

        self.verticalLayout_2.addWidget(self.TypeCombo)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.costLine = QLineEdit(self.centralwidget)
        self.costLine.setObjectName(u"costLine")

        self.verticalLayout_2.addWidget(self.costLine)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.sellPrice = QLineEdit(self.centralwidget)
        self.sellPrice.setObjectName(u"sellPrice")

        self.verticalLayout_2.addWidget(self.sellPrice)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.quantityLine = QLineEdit(self.centralwidget)
        self.quantityLine.setObjectName(u"quantityLine")

        self.verticalLayout_2.addWidget(self.quantityLine)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)

        self.quantityLimitLine = QLineEdit(self.centralwidget)
        self.quantityLimitLine.setObjectName(u"quantityLimitLine")

        self.verticalLayout_2.addWidget(self.quantityLimitLine)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cancelButton = QPushButton(self.centralwidget)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.saveButton = QPushButton(self.centralwidget)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.clicked.connect(self.saveButtonClicked)

        self.horizontalLayout_2.addWidget(self.saveButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u039a\u03c9\u03b4\u03b9\u03ba\u03cc\u03c2: ", None))
        self.product_code_label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u038c\u03bd\u03bf\u03bc\u03b1:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u03a4\u03cd\u03c0\u03bf\u03c2:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u039a\u03cc\u03c3\u03c4\u03bf\u03c2 \u0391\u03b3\u03bf\u03c1\u03ac\u03c2:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u03a4\u03b9\u03bc\u03ae \u03c0\u03ce\u03bb\u03b7\u03c3\u03b7\u03c2:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u03a0\u03bf\u03c3\u03cc\u03c4\u03b7\u03c4\u03b1:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u038c\u03c1\u03b9\u03bf \u03c0\u03bf\u03c3\u03cc\u03c4\u03b7\u03c4\u03b1\u03c2:", None))
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03ba\u03cd\u03c1\u03c9\u03c3\u03b7", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"\u0391\u03c0\u03bf\u03b8\u03ae\u03ba\u03b5\u03c5\u03c3\u03b7", None))

    def cancelButtonClicked(self):
        self.close()
    
    def saveButtonClicked(self):
        product_code = self.product_code_label.text()
        name = self.nameLine.text()
        type = self.TypeCombo.currentText()
        cost = self.costLine.text()
        sell_price = self.sellPrice.text()
        quantity = self.quantityLine.text()
        quantity_limit = self.quantityLimitLine.text()

        self.db_manager.insert_product(product_code, name, type, cost, sell_price, quantity, quantity_limit)
        self.close()
    
    def close(self):
        self.db_manager.close()
        sys.exit()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize database manager
        self.db_manager = DatabaseManager('products.db')

        self.product_code = self.db_manager.get_new_product_code()
        self.ui.product_code_label.setText(str(self.product_code))

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

