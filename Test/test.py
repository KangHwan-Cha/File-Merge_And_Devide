from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication

class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemChanged.connect(self.handle_item_changed)

    def handle_item_changed(self, item):
        count = self.count()
        print(f"List count changed: {count}")

if __name__ == "__main__":
    app = QApplication([])
    list_widget = MyListWidget()
    for i in range(10):
        list_widget.addItem(QListWidgetItem(f"Item {i}"))
    list_widget.addItem(QListWidgetItem("New item"))
    list_widget.takeItem(0)
    app.exec_()