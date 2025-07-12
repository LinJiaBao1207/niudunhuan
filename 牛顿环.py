import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QIcon, QPixmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 获取图片
def get_resource_path(relative_path):
    """获取资源的绝对路径。"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 使用示例
icon_path = get_resource_path('niu1.ico')
image_path = get_resource_path('jimei.png')  # 图片路径
yuanli_image_path = get_resource_path('yuanli.jpg')  # 新增图片路径

class Ui_MainWindow(object):
    def wavelength_to_color(self, wavelength):
        if 380 <= wavelength <= 750:
            if wavelength < 440:
                r = -(wavelength - 440) / (440 - 380)
                g = 0
                b = 1
            elif wavelength < 490:
                r = 0
                g = (wavelength - 440) / (490 - 440)
                b = 1
            elif wavelength < 510:
                r = 0
                g = 1
                b = -(wavelength - 510) / (510 - 490)
            elif wavelength < 580:
                r = (wavelength - 510) / (580 - 510)
                g = 1
                b = 0
            elif wavelength < 645:
                r = 1
                g = -(wavelength - 645) / (645 - 580)
                b = 0
            else:
                r = 1
                g = 0
                b = 0
            return (r, g, b)
        else:
            return (0, 0, 0)

    def saveFigure(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "保存图片", "", "Image files (*.png *.xpm *.jpg)",
                                                            options=options)
        if fileName:
            self.fig.savefig(fileName)
            QtWidgets.QMessageBox.information(None, "保存成功", "图片已保存到：\n" + fileName)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(1000, 600)
        MainWindow.setMaximumSize(1000, 600)
        MainWindow.setStyleSheet("background-color: #E9EBFE;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        icon = QIcon(icon_path)
        MainWindow.setWindowIcon(icon)

        # 设置字体
        big_font = QFont()
        big_font.setPointSize(16)
        big_font.setBold(True)
        big_font.setFamily("楷体")

        # 创建状态栏
        self.statusbar = QtWidgets.QStatusBar()
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: white; 
                min-height: 35px;
            }
        """)
        self.status_label = QtWidgets.QLabel("本项目由大学生创新创业训练计划项目赞助")
        self.status_label.setAlignment(QtCore.Qt.AlignRight)
        self.status_label.setStyleSheet("font-size: 24px; font-family: 楷体;")
        self.statusbar.addWidget(self.status_label, 1)

        # 左侧参数输入区
        self.left_layout = QtWidgets.QVBoxLayout()

        # 添加图片
        image_label = QtWidgets.QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(600, 100)  # 设置固定的宽度和高度
        image_label.setPixmap(pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)  # 设置图片居中显示
        self.left_layout.addWidget(image_label)

        # 介绍文本与原理图片两列布局
        text_image_layout = QtWidgets.QHBoxLayout()

        # 左列文本
        introduction_label = QtWidgets.QLabel(
            "  光绘牛顿V1.1是一款用于模\n"
            "拟牛顿环现象的应用程序。通\n"
            "过调整波长、曲率半径、折射\n"
            "率和两个平面之间的距离等参\n"
            "数，观察到牛顿环图案的变化，\n"
            "从而深入理解光学干涉。\n"
            )
        introduction_label.setAlignment(QtCore.Qt.AlignLeft)  # 设置文本居左
        introduction_label.setStyleSheet("""
            QLabel {
                font-size: 25px;
                text-align: left;
                font-family:楷体;
                color: #4B4B4B;
            }
        """)
        text_image_layout.addWidget(introduction_label)

        # 右列图片
        yuanli_image_label = QtWidgets.QLabel()
        yuanli_pixmap = QPixmap(yuanli_image_path)
        yuanli_pixmap = yuanli_pixmap.scaled(200, 200)  # 设置图片宽度和高度
        yuanli_image_label.setPixmap(yuanli_pixmap)
        yuanli_image_label.setAlignment(QtCore.Qt.AlignCenter)
        text_image_layout.addWidget(yuanli_image_label)

        self.left_layout.addLayout(text_image_layout)

        self.left_layout.addStretch()

        # 调整参数标签
        self.adjustment_label = QtWidgets.QLabel("调整参数：")
        self.adjustment_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size:35px;
                font-family:楷体;
                color: #4B4B4B;
            }
        """)
        self.left_layout.addWidget(self.adjustment_label)

        # 创建参数行
        self.parameter_layouts = []

        # 波长（nm）
        self.create_parameter_row("波长λ（nm）：", 380, 750, 600, self.slider_wavelength_value_changed)

        # 曲率半径（m）
        self.create_parameter_row("曲率半径R（m）：", 1, 5, 3, self.slider_radius_value_changed)

        # 折射率（1-5）
        self.create_parameter_row("折射率n：", 10, 50, 20, self.slider_refractive_index_value_changed)

        # 距离（μm）
        self.create_parameter_row("距离e（μm）：", 1, 15, 5, self.slider_gap_value_changed)

        # 右绘图区域
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor('#DCE2F1')
        self.canvas = FigureCanvas(self.fig)

        # 右侧布局
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(self.canvas)

        # 按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()

        self.pushButton = QtWidgets.QPushButton("绘图")
        self.pushButton.clicked.connect(self.plotRings)
        self.pushButton.setFixedWidth(200)
        self.pushButton.setFixedHeight(60)
        self.pushButton.setFont(big_font)
        self.pushButton.setStyleSheet("background-color: #DCE2F1; border-radius: 10px;")
        self.button_layout.addWidget(self.pushButton)

        self.saveButton = QtWidgets.QPushButton("存盘")
        self.saveButton.clicked.connect(self.saveFigure)
        self.saveButton.setFixedWidth(200)
        self.saveButton.setFixedHeight(60)
        self.saveButton.setFont(big_font)
        self.saveButton.setStyleSheet("background-color: #DCE2F1; border-radius: 10px;")
        self.button_layout.addWidget(self.saveButton)

        self.right_layout.addLayout(self.button_layout)

        # 布局组合
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 初始绘制
        self.plotRings()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "光绘牛顿 V1.1"))

    def create_parameter_row(self, label_text, min_value, max_value, initial_value, value_changed_method):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size:30px;
                font-family:楷体;
                color: #4B4B4B;
            }
        """)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(min_value, max_value)
        slider.setValue(initial_value)

        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #ccc;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #FFF2E2;
                border: 1px solid #5c5c5c;
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
        """)

        input_box = QtWidgets.QLineEdit()
        input_box.setText(str(initial_value))
        input_box.setFixedWidth(100)
        input_box.setFont(QFont("Arial", 16))

        slider.valueChanged.connect(lambda: value_changed_method(slider, input_box))
        input_box.editingFinished.connect(lambda: self.update_slider_from_input(slider, input_box, min_value, max_value, value_changed_method))

        layout.addWidget(label)
        layout.addWidget(slider)
        layout.addWidget(input_box)
        layout.addSpacing(20)

        self.left_layout.addLayout(layout)
        self.parameter_layouts.append((slider, input_box))

    def update_slider_from_input(self, slider, input_box, min_value, max_value, value_changed_method):
        try:
            value = float(input_box.text())
            if min_value <= value <= max_value:
                slider.setValue(int(value))
                value_changed_method(slider, input_box)
            else:
                QtWidgets.QMessageBox.warning(None, "警告", f"输入值应在 {min_value} 到 {max_value} 之间。")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "警告", "请输入有效的数值。")

    def slider_wavelength_value_changed(self, slider, input_box):
        input_box.setText(str(slider.value()))
        self.plotRings()

    def slider_radius_value_changed(self, slider, input_box):
        input_box.setText(str(slider.value()))
        self.plotRings()

    def slider_refractive_index_value_changed(self, slider, input_box):
        input_box.setText(str(slider.value() / 10))
        self.plotRings()

    def slider_gap_value_changed(self, slider, input_box):
        input_box.setText(str(slider.value()))
        self.plotRings()

    def plotRings(self):
        try:
            wavelength = float(self.parameter_layouts[0][0].value()) * 1e-9
            radius = float(self.parameter_layouts[1][0].value())
            refractive_index = float(self.parameter_layouts[2][0].value()) / 10
            gap = float(self.parameter_layouts[3][0].value()) * 1e-6

            effective_gap = gap * (1 - (1 / refractive_index))
            r_max = np.sqrt(4 * radius * wavelength) * 2.0
            x = np.linspace(-r_max, r_max, 1500)
            y = np.linspace(-r_max, r_max, 1500)

            X, Y = np.meshgrid(x, y)
            R = np.sqrt((X / radius) ** 2 + (Y / radius) ** 2)

            I_delta = (2 * np.pi * R ** 2) / (radius * wavelength) + (2 * np.pi * effective_gap / wavelength)
            I = 2 * (np.sin(I_delta * refractive_index)) ** 2
            I = I / np.max(I)

            color = self.wavelength_to_color(self.parameter_layouts[0][0].value())
            I_colored = np.zeros((I.shape[0], I.shape[1], 3))
            I_colored[..., 0] = I * color[0]
            I_colored[..., 1] = I * color[1]
            I_colored[..., 2] = I * color[2]

            self.ax.clear()
            self.ax.imshow(I_colored, extent=(-r_max, r_max, -r_max, r_max), origin='lower')
            self.ax.axis('off')
            self.canvas.draw()
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
