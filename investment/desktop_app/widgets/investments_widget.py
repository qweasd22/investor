from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class InvestmentsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент", "Бумага", "Количество", "Депозит"])
        
        self.refresh_btn = QPushButton("Обновить данные")
        self.refresh_btn.clicked.connect(self.load_data)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

    def load_data(self):
        try:
            investments = self.api_client.get_investments()
            self.table.setRowCount(len(investments))

            for row, investment in enumerate(investments):
                self.table.setItem(row, 0, QTableWidgetItem(str(investment['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(investment['client'])))
                self.table.setItem(row, 2, QTableWidgetItem(investment['security']))
                self.table.setItem(row, 3, QTableWidgetItem(str(investment['amount'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(investment['deposit'])))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            self.close()