from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from widgets.clients_widget import ClientsTab
from widgets.securities_widget import SecuritiesTab
from widgets.investments_widget import InvestmentsTab
from widgets.deposits_widget import DepositsTab
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Управление инвестициями")
        self.setMinimumSize(1024, 768)
        
        tabs = QTabWidget()
        tabs.addTab(ClientsTab(self.api_client), "Клиенты")
        tabs.addTab(SecuritiesTab(self.api_client), "Бумаги")
        tabs.addTab(InvestmentsTab(self.api_client), "Инвестиции")
        tabs.addTab(DepositsTab(self.api_client), "Депозиты")

        
        
        self.setCentralWidget(tabs)

    def load_data(self):
        try:
            services = self.api_client.get_clients()  # Исправлено присваивание
            if not services:
                raise Exception("Нет данных для отображения")
        except Exception as e:  # Исправлено имя переменной
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            self.close()