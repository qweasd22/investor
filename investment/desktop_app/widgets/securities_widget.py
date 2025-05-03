from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class SecuritiesTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Код", "Тип", "Минимальная сумма", "Рейтинг", "Годовая доходность", "Издатель"])
        
        self.refresh_btn = QPushButton("Обновить данные")
        self.refresh_btn.clicked.connect(self.load_data)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

    def load_data(self):
        try:
            securities = self.api_client.get_securities()
            self.table.setRowCount(len(securities))

            for row, security in enumerate(securities):
                self.table.setItem(row, 0, QTableWidgetItem(str(security['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(security['name']))
                self.table.setItem(row, 2, QTableWidgetItem(security['code']))
                self.table.setItem(row, 3, QTableWidgetItem(security['security_type']))
                self.table.setItem(row, 4, QTableWidgetItem(str(security['min_amount'])))
                self.table.setItem(row, 5, QTableWidgetItem(str(security['rating'])))
                self.table.setItem(row, 6, QTableWidgetItem(str(security['last_year_yield'])))
                self.table.setItem(row, 7, QTableWidgetItem(str(security['issuer'])))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            self.close()