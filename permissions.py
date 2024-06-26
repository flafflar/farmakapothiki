from PySide6.QtWidgets import QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt
from database import DatabaseManager, UserPermissions

class PermissionsLayout(QVBoxLayout):
    """Custom layout for managing user permissions."""
    def __init__(self, username=None):
        """Initialize the PermissionsLayout."""
        super().__init__()
        self.username = username
        self.db = DatabaseManager()

        self.addWidget(QLabel("Δικαιώματα:"))
        self.permission_checkboxes = []
        
        # Permission names
        self.permissions = [
            "Προβολή στοκ",
            "Επεξεργασία στοκ", 
            "Προσθήκη/Επεξεργασία προϊόντων",                              
            "Προβολή ειδοποιήσεων",
            "Δημιουργία πελατολογίου",
            "Προβολή παραγγελιών",
            "Καταχώρηση παραγγελιών",
            "Αλλαγή κατάστασης παραγγελίας",
            "Προβολή τιμολογίων",
            "Έκδοση τιμολογίων",
            "Προβολή αμοιβών πωλητών",
            "Διαχείριση χρηστών"
        ]

        # Permission names on DataBase
        self.permission_columns = [
            "view_stock",
            "edit_stock",
            "add_products",
            "view_notifications",
            "create_client_list",
            "view_orders",
            "add_orders",
            "change_order_state",
            "view_bills",
            "create_bills",
            "view_salaries",
            "user_administration"
        ]

        #---Add checkboxes
        for permission in self.permissions:
            checkbox = QCheckBox(permission)
            self.permission_checkboxes.append(checkbox)
            self.addWidget(checkbox)

        #---Nested Permissions
        nested_permissions = [1, 6, 7, 9]
        for index in nested_permissions:
            self.permission_checkboxes[index].setEnabled(False)
            self.permission_checkboxes[index].setStyleSheet("QCheckBox { margin-left: 10px; }")

        #---Some permissions enable/disable other permissions
        self.permission_checkboxes[0].stateChanged.connect(lambda state, index=1, checkbox=self.permission_checkboxes[0]: self.enable_permission(checkbox, index))
        self.permission_checkboxes[5].stateChanged.connect(lambda state, index=6, checkbox=self.permission_checkboxes[5]: self.enable_permission(checkbox, index))
        self.permission_checkboxes[5].stateChanged.connect(lambda state, index=7, checkbox=self.permission_checkboxes[5]: self.enable_permission(checkbox, index))
        self.permission_checkboxes[8].stateChanged.connect(lambda state, index=9, checkbox=self.permission_checkboxes[8]: self.enable_permission(checkbox, index))

        self.load_permissions(self.username)

        for index, checkbox in enumerate(self.permission_checkboxes):
            checkbox.stateChanged.connect(lambda state, idx=index: self.update_permission(idx, state))
            
    def load_permissions(self, username):
        """Load permissions from the database for the given user."""
        self.username = username
        user = self.db.get_user_by_username(self.username)
        if user:
            permissions = user.permissions
            for index, checkbox in enumerate(self.permission_checkboxes):
                checkbox.setChecked(getattr(permissions, self.permission_columns[index]))

    def enable_permission(self, checkbox, target_index):
        """Enable or disable a permission checkbox based on another checkbox's state."""
        if checkbox.isChecked():
            self.permission_checkboxes[target_index].setEnabled(True)
        else:
            self.permission_checkboxes[target_index].setEnabled(False)
            self.permission_checkboxes[target_index].setChecked(False)
            
    def update_permission(self, index, state):
        """Update permission value in the database when a checkbox is toggled."""
        column_name = self.permission_columns[index]
        checkbox = self.permission_checkboxes[index]
        value = 1 if checkbox.isChecked() else 0

        user = self.db.get_user_by_username(self.username)
        if user:
            permissions = getattr(user, 'permissions', UserPermissions())
            setattr(permissions, column_name, value)
            user.permissions = permissions
            self.db.update_user(user)

    def get_permissions(self):
        """Get the current permission values."""
        permissions = UserPermissions()

        for index, checkbox in enumerate(self.permission_checkboxes):
            column_name = self.permission_columns[index]
            value = 1 if checkbox.isChecked() else 0
            setattr(permissions, column_name, value)
        return permissions