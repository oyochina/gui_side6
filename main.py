import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QDateTimeEdit, 
                               QTextEdit, QPushButton, QGroupBox, QGridLayout,
                               QListWidget, QListWidgetItem, QSpinBox, QCheckBox)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QIcon


class DeviceControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设备控制界面")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧控制面板
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 右侧显示面板
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QComboBox, QDateTimeEdit, QSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QTextEdit, QListWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
        """)

    def create_left_panel(self):
        """创建左侧控制面板"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # 时间选择组
        time_group = QGroupBox("时间设置")
        time_layout = QGridLayout(time_group)
        
        # 开始时间
        time_layout.addWidget(QLabel("开始时间:"), 0, 0)
        self.start_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        time_layout.addWidget(self.start_time_edit, 0, 1)
        
        # 结束时间
        time_layout.addWidget(QLabel("结束时间:"), 1, 0)
        self.end_time_edit = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        time_layout.addWidget(self.end_time_edit, 1, 1)
        
        # 时间间隔
        time_layout.addWidget(QLabel("时间间隔(秒):"), 2, 0)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3600)
        self.interval_spin.setValue(60)
        time_layout.addWidget(self.interval_spin, 2, 1)
        
        layout.addWidget(time_group)
        
        # 设备选择组
        device_group = QGroupBox("设备选择")
        device_layout = QVBoxLayout(device_group)
        
        # 设备类型选择
        device_layout.addWidget(QLabel("设备类型:"))
        self.device_type_combo = QComboBox()
        self.device_type_combo.addItems(["温度传感器", "湿度传感器", "压力传感器", "流量计", "阀门"])
        device_layout.addWidget(self.device_type_combo)
        
        # 设备列表
        device_layout.addWidget(QLabel("可用设备:"))
        self.device_list = QListWidget()
        self.device_list.setSelectionMode(QListWidget.MultiSelection)
        self.update_device_list()
        device_layout.addWidget(self.device_list)
        
        # 设备控制按钮
        device_buttons_layout = QHBoxLayout()
        self.refresh_devices_btn = QPushButton("刷新设备")
        self.refresh_devices_btn.clicked.connect(self.update_device_list)
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.clicked.connect(self.select_all_devices)
        device_buttons_layout.addWidget(self.select_all_btn)
        
        device_layout.addLayout(device_buttons_layout)
        
        layout.addWidget(device_group)
        
        # 操作控制组
        control_group = QGroupBox("操作控制")
        control_layout = QVBoxLayout(control_group)
        
        # 操作选项
        self.auto_start_check = QCheckBox("自动启动")
        self.auto_start_check.setChecked(True)
        control_layout.addWidget(self.auto_start_check)
        
        self.log_enabled_check = QCheckBox("启用日志记录")
        self.log_enabled_check.setChecked(True)
        control_layout.addWidget(self.log_enabled_check)
        
        # 操作按钮
        self.start_btn = QPushButton("开始监控")
        self.start_btn.clicked.connect(self.start_monitoring)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("停止监控")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("清除日志")
        self.clear_btn.clicked.connect(self.clear_log)
        control_layout.addWidget(self.clear_btn)
        
        layout.addWidget(control_group)
        layout.addStretch()
        
        return left_widget

    def create_right_panel(self):
        """创建右侧显示面板"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # 状态显示组
        status_group = QGroupBox("系统状态")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("系统就绪")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
        
        # 日志显示组
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # 数据显示组
        data_group = QGroupBox("实时数据")
        data_layout = QVBoxLayout(data_group)
        
        self.data_list = QListWidget()
        data_layout.addWidget(self.data_list)
        
        layout.addWidget(data_group)
        
        return right_widget

    def update_device_list(self):
        """更新设备列表"""
        self.device_list.clear()
        device_type = self.device_type_combo.currentText()
        
        # 模拟设备数据
        devices = {
            "温度传感器": ["TEMP_001", "TEMP_002", "TEMP_003", "TEMP_004"],
            "湿度传感器": ["HUM_001", "HUM_002", "HUM_003"],
            "压力传感器": ["PRESS_001", "PRESS_002"],
            "流量计": ["FLOW_001", "FLOW_002", "FLOW_003"],
            "阀门": ["VALVE_001", "VALVE_002", "VALVE_003", "VALVE_004"]
        }
        
        for device in devices.get(device_type, []):
            item = QListWidgetItem(f"{device} - {device_type}")
            self.device_list.addItem(item)

    def select_all_devices(self):
        """选择所有设备"""
        for i in range(self.device_list.count()):
            self.device_list.item(i).setSelected(True)

    def start_monitoring(self):
        """开始监控"""
        selected_devices = [item.text() for item in self.device_list.selectedItems()]
        if not selected_devices:
            self.log_message("警告: 请选择至少一个设备")
            return
        
        start_time = self.start_time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        end_time = self.end_time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        interval = self.interval_spin.value()
        
        self.log_message(f"开始监控 - 时间范围: {start_time} 到 {end_time}")
        self.log_message(f"监控间隔: {interval} 秒")
        self.log_message(f"选中设备: {', '.join(selected_devices)}")
        
        self.status_label.setText("监控中...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # 模拟数据更新
        self.update_data_display()

    def stop_monitoring(self):
        """停止监控"""
        self.log_message("停止监控")
        self.status_label.setText("系统就绪")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def clear_log(self):
        """清除日志"""
        self.log_text.clear()
        self.data_list.clear()
        self.log_message("日志已清除")

    def log_message(self, message):
        """添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

    def update_data_display(self):
        """更新数据显示"""
        import random
        from datetime import datetime
        
        self.data_list.clear()
        selected_devices = [item.text() for item in self.device_list.selectedItems()]
        
        for device in selected_devices:
            # 模拟传感器数据
            if "TEMP" in device:
                value = random.uniform(20.0, 30.0)
                unit = "°C"
            elif "HUM" in device:
                value = random.uniform(40.0, 80.0)
                unit = "%"
            elif "PRESS" in device:
                value = random.uniform(1.0, 2.0)
                unit = "bar"
            elif "FLOW" in device:
                value = random.uniform(10.0, 100.0)
                unit = "L/min"
            else:
                value = random.choice([0, 1])
                unit = "状态"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            item_text = f"[{timestamp}] {device}: {value:.2f} {unit}"
            self.data_list.addItem(item_text)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("设备控制界面")
    app.setApplicationVersion("1.0")
    
    # 创建并显示主窗口
    window = DeviceControlApp()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
