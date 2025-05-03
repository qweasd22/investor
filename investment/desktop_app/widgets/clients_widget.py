from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class ClientsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Тип", "Телефон", "Адрес"
        ])
        
        self.refresh_btn = QPushButton("Обновить данные")
        self.refresh_btn.clicked.connect(self.load_data)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

    def load_data(self):
       try:
           clients = self.api_client.get_clients()
           self.table.setRowCount(len(clients))

           for row, client in enumerate(clients):
               self.table.setItem(row, 0, QTableWidgetItem(str(client['id'])))
               self.table.setItem(row, 1, QTableWidgetItem(client['name']))
               self.table.setItem(row, 2, QTableWidgetItem(client['ownership_type']))
               self.table.setItem(row, 3, QTableWidgetItem(client['phone']))
               self.table.setItem(row, 4, QTableWidgetItem(client['address']))

       except Exception as e:
           QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
           self.close()