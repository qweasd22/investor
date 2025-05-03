from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class DepositsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент",  "Количество", "Рейтинг"])
        
        self.refresh_btn = QPushButton("Обновить данные")
        self.refresh_btn.clicked.connect(self.load_data)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)
        
    def load_data(self):
        try:
            deposits = self.api_client.get_deposits()
            self.table.setRowCount(len(deposits))

            for row, deposit in enumerate(deposits):
                self.table.setItem(row, 0, QTableWidgetItem(str(deposit['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(deposit['client'])))
                self.table.setItem(row, 2, QTableWidgetItem(str(deposit['amount'])))
                self.table.setItem(row, 3, QTableWidgetItem(str(deposit['interest_rate'])))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            self.close()

    