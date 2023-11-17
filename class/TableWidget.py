import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
import pandas as pd

class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setRowCount(len(self.df.index))
        self.setColumnCount(len(self.df.columns))
        self.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iat[i,j]))
                self.setItem(i, j, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    df = pd.DataFrame({'Column 1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11], 'Column 2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11]})
    table_widget = TableWidget(df)
    table_widget.show()
    sys.exit(app.exec_())