from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDialogButtonBox
)

class ClientDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Новый клиент")
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["ООО", "ИП", "АО"])
        self.address_input = QTextEdit()
        self.phone_input = QLineEdit()
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow("Название:", self.name_input)
        layout.addRow("Тип:", self.type_input)
        layout.addRow("Адрес:", self.address_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow(buttons)
        
        self.setLayout(layout)