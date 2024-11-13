#python -m PyQt6.uic.pyuic -x k.ui -o ui.py

import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel, QFileDialog
import PyQt6.QtWidgets as QtWidgets
from ui import Ui_MainWindow
from algorithm import GreedyTSP  # Sử dụng GreedyTSP thay vì Hill Climbing
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QCoreApplication, QTimer
import qtinter
import random
import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
import time
import csv

class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.setModal(True)
        self.layout = QVBoxLayout()
        if message is None:
            self.message = QLabel("Please enter the number of destinations")
        else:
            self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.setLayout(self.layout)

class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btStart.clicked.connect(self.start)
        self.ui.btStop.clicked.connect(self.stop)
        self.ui.btSave = QtWidgets.QPushButton(self.ui.centralwidget)
        self.ui.btSave.setGeometry(550, 420, 100, 40)
        self.ui.btSave.setText("Lưu kết quả")
        self.ui.btSave.setStyleSheet("background-color: #2196F3; color: white; border-radius: 10px;")
        self.ui.btSave.clicked.connect(self.save_result)

        self.ui.btLoad = QtWidgets.QPushButton(self.ui.centralwidget)
        self.ui.btLoad.setGeometry(670, 420, 100, 40)
        self.ui.btLoad.setText("Tải kết quả")
        self.ui.btLoad.setStyleSheet("background-color: #FF9800; color: white; border-radius: 10px;")
        self.ui.btLoad.clicked.connect(self.load_result)

        self.task = None
        self.ui.progressBar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start(self):
        if not self.isRunning:
            self.isRunning = True
            self.ui.canvaFrame.setVisible(True)
            self.ui.label_status.setText("Trạng thái: Đang chạy...")
            self.ui.progressBar.setValue(0)
            self.timer.start(100)  # Cập nhật tiến trình mỗi 100ms
            print("Start")

            # Thực hiện giải thuật Greedy
            tsp = GreedyTSP(int(self.ui.spinBox.value()))
            start_time = time.time()
            path = tsp.solve()
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Cập nhật thông tin kết quả
            self.ui.tbResult.setText(f"{tsp.result}\nThời gian chạy: {elapsed_time:.2f} giây")
            self.ui.canvaFrame.canvas.axes.clear()

            # Vẽ đồ thị minh họa (gọi hàm tạo đồ thị trong GreedyTSP)
            tsp.create_plot()
            self.ui.canvaFrame.canvas.draw()  # Cập nhật canvas sau khi vẽ

            self.ui.label_status.setText("Trạng thái: Hoàn thành!")
            self.ui.progressBar.setValue(100)
            self.timer.stop()

        else:
            dlg = AlertDialog("Vui lòng dừng lại đoạn code")
            dlg.exec()

    def stop(self):
        if self.isRunning:
            self.isRunning = False
            print("Stop")
            self.ui.tbResult.setText("")
            self.ui.canvaFrame.setVisible(False)
            self.ui.label_status.setText("Trạng thái: Đã dừng")
            self.ui.progressBar.setValue(0)
            self.timer.stop()

    def save_result(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Lưu kết quả", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Path", "Total Distance", "Steps", "Elapsed Time"])
                tsp_result = self.ui.tbResult.toPlainText().splitlines()
                if len(tsp_result) >= 4:
                    path_info = tsp_result[0].split(': ')[1] if len(tsp_result[0].split(': ')) > 1 else ""
                    total_distance = tsp_result[1].split(': ')[1] if len(tsp_result[1].split(': ')) > 1 else ""
                    steps = tsp_result[2].split(': ')[1] if len(tsp_result[2].split(': ')) > 1 else ""
                    elapsed_time = tsp_result[3].split(': ')[1] if len(tsp_result[3].split(': ')) > 1 else ""
                    writer.writerow([path_info, total_distance, steps, elapsed_time])

    def load_result(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Tải kết quả", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Bỏ qua tiêu đề
                for row in reader:
                    path_info, total_distance, steps, elapsed_time = row
                    self.ui.tbResult.setText(f"Đường đi: {path_info}\nTổng độ dài: {total_distance}\nSố bước: {steps}\nThời gian chạy: {elapsed_time}")

    def update_progress(self):
        current_value = self.ui.progressBar.value()
        if current_value < 100:
            self.ui.progressBar.setValue(current_value + 5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Core()
    plt.axis('off')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    with qtinter.using_qt_from_asyncio():
        window.show()
        sys.exit(app.exec())
