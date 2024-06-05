from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from admin_window import AdministrationWindow
from companies import CompaniesWindow
from categories import CategoriesWindow
from clients_personal import PersonalClientsWindow

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle(" ")
        self.resize(800, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 0, 40, 50)

        upper_hbox = QHBoxLayout()
        upper_hbox.addStretch()

        b_username = QPushButton(username)
        b_username.setIcon(QPixmap("icons/icon_user.png"))

        b_notifications = QPushButton("Ειδοποιήσεις")
        b_logout = QPushButton("Αποσύνδεση")

        upper_hbox.addWidget(b_username)
        upper_hbox.addWidget(b_notifications)
        upper_hbox.addWidget(b_logout)

        main_layout.addLayout(upper_hbox)

        lower_hbox = QHBoxLayout()

        vbox1 = QVBoxLayout()
        vbox1.setAlignment(Qt.AlignTop)

        # Function to create label with image
        def create_label_with_image_and_line(text, image_path):
            hbox = QHBoxLayout()
            hbox.setSpacing(10)  # Adjust spacing between icon and text

            pixmap = QPixmap(image_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)

            text_label = QLabel(text)
            text_label.setAlignment(Qt.AlignLeft)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            # Add icon and text to hbox
            hbox.addWidget(image_label)
            hbox.addWidget(text_label)
            hbox.addStretch()  # Push the line to the end

            vbox = QVBoxLayout()
            vbox.addLayout(hbox)
            vbox.addWidget(line)

            return vbox

        # Storage section
        storage_vbox = create_label_with_image_and_line("Αποθήκη", "icons/m_apothiki.png")
        b_viewStock = QPushButton("Προβολή στοκ")
        b_addNewReceipt = QPushButton("Προσθήκη νέας παραλαβής")

        # Products section
        products_vbox = create_label_with_image_and_line("Προϊόντα", "icons/m_proionta.png")
        b_viewProducts = QPushButton("Προβολή προϊόντων")
        b_addNewProduct = QPushButton("Προσθήκη νέου προϊόντος")
        b_editCategories = QPushButton("Επεξεργασία κατηγοριών")
        b_editCompanies = QPushButton("Επεξεργασία εταιρειών")

        # Admin section
        admin_vbox = create_label_with_image_and_line("Διαχείριση", "icons/m_diaxirisi.png")
        b_userAdministration = QPushButton("Διαχείριση χρηστών")
        b_viewSalaries = QPushButton("Προβολή αμοιβών πωλητών")

        # Adding widgets to the first VBox
        vbox1.addLayout(storage_vbox)
        vbox1.addWidget(b_viewStock)
        vbox1.addWidget(b_addNewReceipt)

        vbox1.addLayout(products_vbox)
        vbox1.addWidget(b_viewProducts)
        vbox1.addWidget(b_addNewProduct)
        vbox1.addWidget(b_editCategories)
        vbox1.addWidget(b_editCompanies)

        vbox1.addLayout(admin_vbox)
        vbox1.addWidget(b_userAdministration)
        vbox1.addWidget(b_viewSalaries)

        vbox1.addStretch()
        lower_hbox.addLayout(vbox1)

        lower_hbox.addSpacing(20)  # Add space between the two vboxes

        vbox2 = QVBoxLayout()
        vbox2.setAlignment(Qt.AlignTop)

        # Clients section
        clients_vbox = create_label_with_image_and_line("Πελάτες", "icons/m_pelates.png")
        b_viewClients = QPushButton("Προβολή πελατολογίου")

        # Orders section
        orders_vbox = create_label_with_image_and_line("Παραγγελίες", "icons/m_paraggelies.png")
        b_addNewOrder = QPushButton("Προσθήκη νέας παραγγελίας")
        b_viewPendingOrders = QPushButton("Προβολή εκκρεμών παραγγελιών")
        b_viewReadyOrders = QPushButton("Προβολή έτοιμων παραγγελιών")
        b_viewAllOrders = QPushButton("Προβολή όλων των παραγγελιών")

        # Bills section
        bills_vbox = create_label_with_image_and_line("Τιμολόγια", "icons/m_timologia.png")
        b_searchBill = QPushButton("Αναζήτηση τιμολογίου")
        b_viewPendingBills = QPushButton("Προβολή μη εξοφλημένων τιμολογίων")

        # Adding widgets to the second VBox
        vbox2.addLayout(clients_vbox)
        vbox2.addWidget(b_viewClients)

        vbox2.addLayout(orders_vbox)
        vbox2.addWidget(b_addNewOrder)
        vbox2.addWidget(b_viewPendingOrders)
        vbox2.addWidget(b_viewReadyOrders)
        vbox2.addWidget(b_viewAllOrders)

        vbox2.addLayout(bills_vbox)
        vbox2.addWidget(b_searchBill)
        vbox2.addWidget(b_viewPendingBills)

        vbox2.addStretch()
        lower_hbox.addLayout(vbox2)

        main_layout.addLayout(lower_hbox)
#---------------------------------------------------------------------------------------------#
        b_logout.clicked.connect(self.logout)

        b_userAdministration.clicked.connect(self.open_administration_window)
        b_editCategories.clicked.connect(self.open_categories_window)
        b_editCompanies.clicked.connect(self.open_companies_window)
        b_viewClients.clicked.connect(self.open_clients_window)
        #b_viewStock.clicked.connect(self.open_stock_window)
#---------------------------------------------------------------------------------------------#
    def open_administration_window(self):
        """Open the administration window."""
        self.admin_window = AdministrationWindow()
        with open("styles/adminstyles.qss", "r") as f:
           self.admin_window.setStyleSheet(f.read())
        self.admin_window.show()

    def open_categories_window(self):
        """Open the categories window."""
        self.categories = CategoriesWindow()
        with open("styles/styles_categories.qss", "r") as f:
            self.categories.setStyleSheet(f.read())
        self.categories.show()
    
    def open_companies_window(self):
        """Open the companies window."""
        self.companies = CompaniesWindow()
        with open("styles/styles_companies.qss", "r") as f:
            self.companies.setStyleSheet(f.read())
        self.companies.show()

    def open_clients_window(self):
        self.clients = PersonalClientsWindow(self.username)
        with open("styles/styles_clients.qss", "r") as f:
            self.clients.setStyleSheet(f.read())
        self.clients.show()

    def logout(self):
       """Log out of the application."""
       self.close()
       from login_form import LoginForm # import here to avoid circular import
       self.login_window = LoginForm()
       self.login_window.show()