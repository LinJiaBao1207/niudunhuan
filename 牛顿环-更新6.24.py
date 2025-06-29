import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QSlider, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

# 设置字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 图像负号显示

def get_resource_path(relative_path):
    """获取资源的绝对路径。"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)

class NewtonRingsSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 窗口设置
        self.setWindowTitle("Light Painting Newton's RingsV1.0")
        self.setMinimumSize(1200, 1100)
        self.setStyleSheet("background-color: #E9EBFE;")  # 浅灰色背景

        # 主窗口部件
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # ========== 左侧布局 ==========
        self.left_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, stretch=1)

        # 标题
        self.title_label = QtWidgets.QLabel("Newton's Rings Interference\n"
                                            " Simulation Experiment")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 36px;
                font-family: 宋体;
                color: black;
                padding: 10px;
            }
        """)
        self.left_layout.addWidget(self.title_label)

        # 光路图和公式区域
        self.diagram_formula_layout = QtWidgets.QHBoxLayout()

        # 左侧 - 公式和按钮区域
        self.formula_button_group = QtWidgets.QGroupBox()
        self.formula_button_group.setStyleSheet("QGroupBox { border: none; }")
        self.formula_button_layout = QtWidgets.QVBoxLayout()

        # 明环公式图片
        self.bright_formula_frame = QtWidgets.QLabel()
        self.bright_formula_frame.setFixedSize(250, 100)
        bright_formula_path = get_resource_path('image/newton_rings_3_1.png')
        bright_pixmap = QPixmap(bright_formula_path)
        self.bright_formula_frame.setPixmap(bright_pixmap.scaled(250, 100, QtCore.Qt.KeepAspectRatio))
        self.bright_formula_frame.setStyleSheet("""
            QLabel {
                border: 2px dashed gray;
            }
        """)
        self.bright_label = QtWidgets.QLabel("Bright ring radius：")
        self.bright_label.setStyleSheet("font-size: 16px; color: black;")
        self.formula_button_layout.addWidget(self.bright_label)
        self.formula_button_layout.addWidget(self.bright_formula_frame)

        # 暗环公式图片
        self.dark_formula_frame = QtWidgets.QLabel()
        self.dark_formula_frame.setFixedSize(250, 100)
        dark_formula_path = get_resource_path('image/newton_rings_3_2.png')
        dark_pixmap = QPixmap(dark_formula_path)
        self.dark_formula_frame.setPixmap(dark_pixmap.scaled(250, 100, QtCore.Qt.KeepAspectRatio))
        self.dark_formula_frame.setStyleSheet("""
            QLabel {
                border: 2px dashed gray;
            }
        """)
        self.dark_label = QtWidgets.QLabel("Dark ring radius：")
        self.dark_label.setStyleSheet("font-size: 16px; color: black;")
        self.formula_button_layout.addWidget(self.dark_label)
        self.formula_button_layout.addWidget(self.dark_formula_frame)

        # 按钮区域
        self.reset_button = QPushButton("Restore default")
        self.reset_button.setFixedSize(250, 60)
        self.reset_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #F0F0F0;
                color: black;
                font-weight: bold;
            }
        """)
        self.reset_button.clicked.connect(self.reset_parameters)

        self.save_button = QPushButton("Save image")
        self.save_button.setFixedSize(250, 60)
        self.save_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #F0F0F0;
                color: black;
                font-weight: bold;
            }
        """)
        self.save_button.clicked.connect(self.save_figure)

        self.doc_button = QPushButton("Principle document")
        self.doc_button.setFixedSize(250, 60)
        self.doc_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #F0F0F0;
                color: black;
                font-weight: bold;
            }
        """)
        self.doc_button.clicked.connect(self.open_pdf)

        self.formula_button_layout.addWidget(self.reset_button)
        self.formula_button_layout.addWidget(self.save_button)
        self.formula_button_layout.addWidget(self.doc_button)
        self.formula_button_layout.addStretch(1)

        self.formula_button_group.setLayout(self.formula_button_layout)
        self.diagram_formula_layout.addWidget(self.formula_button_group, stretch=1)

        # 右侧 - 光路图
        self.light_path_widget = QtWidgets.QWidget()
        self.light_path_layout = QtWidgets.QVBoxLayout(self.light_path_widget)

        # 光路图绘制区域 (450x400)
        self.fig1 = plt.figure(figsize=(4.5, 4), facecolor='#E9EBFE')
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.setFixedSize(450, 400)
        self.light_path_layout.addWidget(self.canvas1)

        self.description_label = QtWidgets.QLabel(
                                                  "Light Painting Newton V1.0 is an application\n"
                                                  "designedto simulate the phenomenon of Newton's\n"
                                                  "rings. By adjusting parameters such as wavelen-\n"
                                                  "gth,radius of curvature, refractive index, and\n"
                                                  "the distance between the two surfaces, users \n"
                                                  "can observe changes in the Newton's rings patt-\n"
                                                  "ern,gaining a deeper understanding of optical\n"
                                                  "interference.")
        self.description_label.setAlignment(QtCore.Qt.AlignLeft)
        self.description_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 24px;
                font-family: 宋体;
                color: black;
                padding: 10px;
            }
        """)
        self.light_path_layout.addWidget(self.description_label)

        self.diagram_formula_layout.addWidget(self.light_path_widget, stretch=2)
        self.left_layout.addLayout(self.diagram_formula_layout)

        # 参数调整区域
        self.params_group = QtWidgets.QGroupBox("Adjust parameters：")
        self.params_group.setStyleSheet("""
            QGroupBox {
                font-size: 36px;
                font-weight: bold;
                font-family: 宋体;
                color: black;
            }
        """)
        self.params_layout = QtWidgets.QVBoxLayout()

        # 滑块样式
        slider_style = """
            QSlider::groove:horizontal {
                background: #ccc;
                height: 13px;  
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #FFF2E2;
                border: 1px solid #5c5c5c;
                width: 26px;  
                margin: -6px 0;  
                border-radius: 13px;
            }
        """

        # 波长调节 (整数)
        self.wavelength_slider = self.create_parameter_slider("Wavelength λ（nm）：", 380, 750, 589, scale=1)
        self.wavelength_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.wavelength_slider.itemAt(2).widget().setFixedHeight(26)
        self.params_layout.addLayout(self.wavelength_slider)

        # 曲率半径调节 (带1位小数)
        self.radius_slider = self.create_parameter_slider("Radius of curvature R（m）：", 1, 5, 1.5, scale=0.1)
        self.radius_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.radius_slider.itemAt(2).widget().setFixedHeight(26)
        self.params_layout.addLayout(self.radius_slider)

        self.n1_slider = self.create_parameter_slider("Glass refractive index n1：", 1, 2, 1.5, scale=0.1)
        self.n1_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.n1_slider.itemAt(2).widget().setFixedHeight(26)
        self.params_layout.addLayout(self.n1_slider)

        # 空气折射率n2调节 (固定为1.0)
        self.n2_slider = self.create_parameter_slider("Air refractive index n2：", 1, 1, 0.5, scale=0.1)
        self.n2_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.n2_slider.itemAt(2).widget().setFixedHeight(26)
        self.n2_slider.itemAt(2).widget().setText("1.0")  # 固定显示为1.0
        self.n2_slider.itemAt(1).widget().setEnabled(False)  # 禁用滑块
        self.params_layout.addLayout(self.n2_slider)

        # 玻璃折射率n3调节 (带1位小数)
        self.n3_slider = self.create_parameter_slider("Glass refractive index n3：", 1, 2, 1.5, scale=0.1)
        self.n3_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.n3_slider.itemAt(2).widget().setFixedHeight(26)
        self.params_layout.addLayout(self.n3_slider)

        # 实际距离调节 (整数)
        self.gap_slider = self.create_parameter_slider("Actual distance e（μm）：", 1, 15, 5, scale=1)
        self.gap_slider.itemAt(1).widget().setStyleSheet(slider_style)
        self.gap_slider.itemAt(2).widget().setFixedHeight(26)
        self.params_layout.addLayout(self.gap_slider)

        self.params_group.setLayout(self.params_layout)
        self.params_group.setMinimumHeight(320)
        self.left_layout.addWidget(self.params_group)

        # ========== 右侧布局 ==========
        self.right_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.right_layout, stretch=2)

        # 干涉图区域
        self.interference_group = QtWidgets.QWidget()
        self.interference_layout = QtWidgets.QVBoxLayout(self.interference_group)

        # 上侧 - 牛顿环光强图 (500x350)
        self.intensity_fig = plt.figure(figsize=(5, 3.5), facecolor='#E9EBFE')
        self.ax_intensity = self.intensity_fig.add_subplot(111)
        self.canvas_intensity = FigureCanvas(self.intensity_fig)
        self.canvas_intensity.setFixedSize(500, 350)
        self.interference_layout.addWidget(self.canvas_intensity)

        # 下侧 - 牛顿环干涉图 (500x500)
        self.interference_fig = plt.figure(figsize=(5, 5), facecolor='#E9EBFE')
        self.ax_interference = self.interference_fig.add_subplot(111)
        self.canvas_interference = FigureCanvas(self.interference_fig)
        self.canvas_interference.setFixedSize(500, 500)
        self.interference_layout.addWidget(self.canvas_interference)

        self.right_layout.addWidget(self.interference_group)

        # 状态栏
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QtWidgets.QLabel("This project is supported by the Undergraduate Innovation and Entrepreneurship Training Program of Chengyi College, Jimei University.")
        self.status_label.setStyleSheet("font-size: 20px; font-family: 宋体; color: black;")
        self.status_bar.addPermanentWidget(self.status_label)

        # 绘制初始图像
        self.plot_light_path()
        self.plot_intensity_pattern()
        self.plot_interference_pattern()

    def wavelength_to_color(self, wavelength):
        """将波长转换为RGB颜色"""
        if 380 <= wavelength <= 760:
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

    def create_parameter_slider(self, label_text, min_val, max_val, init_val, scale=1):
        """创建参数滑块控件
        scale: 缩放因子，用于将滑块整数值转换为实际值(如0.1表示滑块值除以10)
        """
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 24px;
                font-family: 楷体;
                color: #4B4B4B;
                min-width: 120px;
            }
        """)
        layout.addWidget(label)

        slider = QSlider(QtCore.Qt.Horizontal)
        slider.setRange(int(min_val / scale), int(max_val / scale))
        slider.setValue(int(init_val / scale))
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

        value_label = QtWidgets.QLineEdit(f"{init_val:.1f}" if scale != 1 else str(init_val))
        value_label.setFixedWidth(100)
        value_label.setStyleSheet("font-size: 16px; font-family: Arial;")

        def update_value_label(value):
            actual_value = value * scale
            value_label.setText(f"{actual_value:.1f}" if scale != 1 else str(actual_value))
            self.update_plots()

        slider.valueChanged.connect(update_value_label)

        def validate_input():
            try:
                input_value = float(value_label.text())
                if min_val <= input_value <= max_val:
                    slider.setValue(int(input_value / scale))
                else:
                    QtWidgets.QMessageBox.warning(None, "警告", f"输入值应在 {min_val} 到 {max_val} 之间。")
                    value_label.setText(f"{slider.value() * scale:.1f}" if scale != 1 else str(slider.value()))
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "警告", "请输入有效的数值。")
                value_label.setText(f"{slider.value() * scale:.1f}" if scale != 1 else str(slider.value()))

        value_label.editingFinished.connect(validate_input)

        layout.addWidget(slider, stretch=1)
        layout.addWidget(value_label)

        return layout

    def update_slider_from_input(self, slider, input_box, min_val, max_val):
        """从输入框更新滑块值"""
        try:
            value = float(input_box.text())
            if min_val <= value <= max_val:
                slider.setValue(int(value))
            else:
                QtWidgets.QMessageBox.warning(None, "警告", f"输入值应在 {min_val} 到 {max_val} 之间。")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "警告", "请输入有效的数值。")

    def update_plots(self):
        """更新所有绘图"""
        self.plot_light_path()
        self.plot_intensity_pattern()
        self.plot_interference_pattern()

    def plot_light_path(self):
        """绘制光路图"""
        wavelength = self.wavelength_slider.itemAt(1).widget().value()  # 已经是实际值
        radius = float(self.radius_slider.itemAt(2).widget().text())  # 从文本框获取实际值
        gap = float(self.gap_slider.itemAt(2).widget().text()) / 3  # 从文本框获取实际值

        self.ax1.clear()
        a1 = 12
        b1 = 12 / radius
        h1 = 0
        k1 = 0
        theta1 = 6 * np.pi / 5
        theta2 = 9 * np.pi / 5
        x0 = 0
        y0 = 15
        x1 = a1 * np.cos(theta1) + h1
        y1 = b1 * np.sin(theta1) + k1
        x2 = a1 * np.cos(theta2) + h1
        y2 = b1 * np.sin(theta2) + k1
        y1_1 = - b1
        y2_1 = - b1
        x3 = a1 * np.cos(np.pi) + h1
        y3 = b1 * np.sin(np.pi) + k1
        x4 = a1 * np.cos(2 * np.pi) + h1
        y4 = b1 * np.sin(2 * np.pi) + k1
        theta = np.linspace(np.pi, 2 * np.pi, 1000)
        x_ellipse = a1 * np.cos(theta) + h1
        y_ellipse = b1 * np.sin(theta) + k1
        rect_width = 2 * a1 + 5
        rect_height = 2
        rect_x = h1 - a1 - 5
        rect_y = k1 - b1 - rect_height - gap

        self.ax1.plot(x_ellipse, y_ellipse, color='#A9ABFE', lw=3)
        self.ax1.fill(x_ellipse, y_ellipse, color='#A9ABFE', alpha=0.5)
        rect = plt.Rectangle((rect_x, rect_y), rect_width + 5, rect_height, linewidth=1,
                             edgecolor='#A9ABFE', facecolor='#A9ABFE', lw=3, alpha=0.5)
        self.ax1.add_patch(rect)
        self.ax1.plot([x1 - b1, x2 + b1], [y1, y2], color='black', lw=2, linestyle='--')
        self.ax1.plot([x1 - b1, x2 + b1], [y1_1, y2_1], color='black', lw=2, linestyle='--')
        self.ax1.plot([x3, x4], [y3, y4], color='#A9ABFE', lw=3)
        self.ax1.plot([x0, x0], [y0, -b1], color='black', lw=2)
        self.ax1.plot(x0, -b1, marker='o', markersize=8, color='black')
        self.ax1.text(x0 + 1.5, -b1 - 1.5, 'O', fontsize=24, ha='center', va='center')
        self.ax1.plot(x0, y2, marker='o', markersize=8, color='black')
        self.ax1.text(x0 + 2, y2 - 2, "O'", fontsize=24, ha='center', va='center')
        self.ax1.plot([x0, x2], [y0, y2], color='black', lw=2)
        self.ax1.plot(x2, y2, marker='o', markersize=8, color='black')
        self.ax1.plot([x0, x2], [y2, y2], color='black', lw=3)
        self.ax1.text(x2 / 2, y2 + 1, 'r', fontsize=30, ha='center', va='center')
        self.ax1.text((x0 + x2) / 2 + 1, (y0 + y2) / 2 + 1, 'R', fontsize=24, ha='center', va='center')

        color = self.wavelength_to_color(wavelength)
        self.ax1.text(0, 20, 'Incident Light', fontsize=28, ha='center', va='center')
        self.ax1.annotate('', xy=(x1, 10), xytext=(x1, 18),
                          arrowprops=dict(arrowstyle='-|>', color="red", lw=4))
        self.ax1.annotate('', xy=(-x1, 10), xytext=(-x1, 18),
                          arrowprops=dict(arrowstyle='-|>', color="red", lw=4))
        self.ax1.annotate('', xy=(x1, y1), xytext=(x1, 5),
                          arrowprops=dict(arrowstyle='-|>', color="red", lw=2))
        self.ax1.text(x1, 6, 'a', fontsize=24, ha='center', va='center')
        self.ax1.annotate('', xy=(2 * x1 / 3, 5), xytext=(2 * x1 / 3, y1),
                          arrowprops=dict(arrowstyle='-|>', color="red", lw=3))
        self.ax1.text(2 * x1 / 3, 6, 'b', fontsize=24, ha='center', va='center')
        self.ax1.annotate('', xy=(x1 / 3, 5), xytext=(x1 / 3, -gap - b1),
                          arrowprops=dict(arrowstyle='-|>', color="red", lw=2))
        self.ax1.text(x1 / 3, 6, "b'", fontsize=24, ha='center', va='center')
        self.ax1.annotate('', xy=(x2 + b1, y2), xytext=(x2 + b1, y2_1),
                          arrowprops=dict(arrowstyle='<->', color='black', lw=2))
        self.ax1.text(x2 + b1 + 1, (y2 + y2_1) / 2, 'd', fontsize=24, ha='center', va='center')
        self.ax1.annotate('', xy=(x2 + b1 - 1, y2_1), xytext=(x2 + b1 - 1, y2_1 - gap),
                          arrowprops=dict(arrowstyle='<->', color='black', lw=2))
        self.ax1.text(x2 + b1, y2_1 - gap / 2, 'e', fontsize=24, ha='center', va='center')

        self.ax1.set_aspect('equal', adjustable='box')
        self.ax1.set_xlim(h1 - a1 - 5, h1 + a1 + 5)
        self.ax1.set_ylim(k1 - b1 - 5, k1 + 20)
        self.ax1.axis('off')
        self.canvas1.draw()

    def plot_intensity_pattern(self):
        """绘制牛顿环光强图"""
        wavelength = float(self.wavelength_slider.itemAt(2).widget().text()) * 1e-9
        radius = float(self.radius_slider.itemAt(2).widget().text())
        n1 = float(self.n1_slider.itemAt(2).widget().text())
        n2 = 1.0  # 固定为空气折射率
        n3 = float(self.n3_slider.itemAt(2).widget().text())
        gap = float(self.gap_slider.itemAt(2).widget().text()) * 1e-6

        # 判断是否引入半波损失
        if (n1 > n2 and n2 < n3) or (n1 < n2 and n2 > n3):
            half_wave_loss = np.pi  # 半波损失
        else:
            half_wave_loss = 0  # 无半波损失

        # 计算有效间隙
        effective_gap = gap * (n1 - n2) + gap * (n2 - n3)

        r_max = np.sqrt(4 * radius * wavelength) * 1.0
        r = np.linspace(-r_max, r_max, 1000)

        I_delta = (2 * np.pi * r ** 2) / (radius * wavelength) + (
                    2 * np.pi * effective_gap / wavelength) + half_wave_loss
        I = 2 * (np.sin(I_delta * n1)) ** 2
        I = I / np.max(I)

        self.ax_intensity.clear()
        self.ax_intensity.plot(r, I, color='blue')
        self.ax_intensity.set_title("Newton's rings intensity distribution", fontsize=12, fontfamily='SimHei')

        if not hasattr(self, 'intensity_axis_limits'):
            self.intensity_axis_limits = self.ax_intensity.get_xlim(), self.ax_intensity.get_ylim()
        else:
            xlim, ylim = self.intensity_axis_limits
            self.ax_intensity.set_xlim(xlim)
            self.ax_intensity.set_ylim(ylim)

        self.ax_intensity.set_xlabel("Radius (m)")
        self.ax_intensity.set_ylabel("Relative Light Intensity")
        self.canvas_intensity.draw()

    def plot_interference_pattern(self):
        """绘制牛顿环干涉图"""
        wavelength = float(self.wavelength_slider.itemAt(2).widget().text())
        radius = float(self.radius_slider.itemAt(2).widget().text())
        n1 = float(self.n1_slider.itemAt(2).widget().text())
        n2 = 1.0  # 固定为空气折射率
        n3 = float(self.n3_slider.itemAt(2).widget().text())
        gap = float(self.gap_slider.itemAt(2).widget().text()) * 1e-6

        # 判断是否引入半波损失
        if (n1 > n2 and n2 < n3) or (n1 < n2 and n2 > n3):
            half_wave_loss = np.pi  # 半波损失
        else:
            half_wave_loss = 0  # 无半波损失

        # 计算有效间隙
        effective_gap = gap * (n1 - n2) + gap * (n2 - n3)

        r_max = np.sqrt(4 * radius * wavelength * 1e-9) * 1.0
        x = np.linspace(-r_max, r_max, 500)
        y = np.linspace(-r_max, r_max, 500)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X ** 2 + Y ** 2)

        I_delta = (2 * np.pi * R ** 2) / (radius * wavelength * 1e-9) + \
                  (2 * np.pi * effective_gap / (wavelength * 1e-9)) + half_wave_loss
        I = 2 * (np.sin(I_delta * n1)) ** 2
        I = I / np.max(I)

        color = self.wavelength_to_color(wavelength)
        I_colored = np.zeros((I.shape[0], I.shape[1], 3))
        I_colored[..., 0] = I * color[0]
        I_colored[..., 1] = I * color[1]
        I_colored[..., 2] = I * color[2]

        self.ax_interference.clear()
        self.ax_interference.imshow(I_colored,
                                    extent=(-r_max, r_max, -r_max, r_max),
                                    origin='lower')
        self.ax_interference.set_title("Newton's rings interference pattern", fontsize=12, fontfamily='SimHei')

        if not hasattr(self, 'interference_axis_limits'):
            self.interference_axis_limits = self.ax_interference.get_xlim(), self.ax_interference.get_ylim()
        else:
            xlim, ylim = self.interference_axis_limits
            self.ax_interference.set_xlim(xlim)
            self.ax_interference.set_ylim(ylim)

        self.ax_interference.set_xlabel("x (m)")
        self.ax_interference.set_ylabel("y (m)")
        self.canvas_interference.draw()

    def reset_parameters(self):
        """重置所有参数为默认值"""
        # 重置滑块值
        self.wavelength_slider.itemAt(1).widget().setValue(589)
        self.radius_slider.itemAt(1).widget().setValue(15)
        self.n1_slider.itemAt(1).widget().setValue(15)
        self.n2_slider.itemAt(1).widget().setValue(10)
        self.n3_slider.itemAt(1).widget().setValue(15)
        self.gap_slider.itemAt(1).widget().setValue(5)

        # 更新输入框显示
        self.wavelength_slider.itemAt(2).widget().setText("589")
        self.radius_slider.itemAt(2).widget().setText("1.5")
        self.n1_slider.itemAt(2).widget().setText("1.5")
        self.n2_slider.itemAt(2).widget().setText("1.0")
        self.n3_slider.itemAt(2).widget().setText("1.5")
        self.gap_slider.itemAt(2).widget().setText("5")

        # 更新所有图像
        self.update_plots()

    def open_pdf(self):
        pdf_path = "document\牛顿环干涉文档.pdf"
        if os.path.exists(pdf_path):
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(pdf_path))
        else:
            print("PDF 文件未找到！")

    def save_figure(self):
        """保存当前图像到文件"""
        # 弹出对话框让用户选择要保存的图像类型
        items = ("光路图", "光强图", "干涉图")
        item, ok = QtWidgets.QInputDialog.getItem(
            self,
            "保存图像",
            "请选择要保存的图像类型:",
            items,
            0,
            False
        )

        if not ok or not item:
            return  # 用户取消选择

        # 根据选择确定要保存的图形对象
        if item == "光路图":
            fig = self.fig1
            default_name = "newton_rings_light_path.png"
        elif item == "光强图":
            fig = self.intensity_fig
            default_name = "newton_rings_intensity.png"
        else:  # 干涉图
            fig = self.interference_fig
            default_name = "newton_rings_interference.png"

        # 弹出文件保存对话框
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "保存图像",
            default_name,
            "PNG 图像 (*.png);;JPEG 图像 (*.jpg);;所有文件 (*)",
            options=options
        )

        if file_path:
            try:
                # 确保文件扩展名与选择的过滤器匹配
                if not file_path.endswith(('.png', '.jpg')):
                    if _.startswith('PNG'):
                        file_path += '.png'
                    else:
                        file_path += '.jpg'

                # 保存图像
                fig.savefig(file_path, dpi=300, bbox_inches='tight')

                # 显示保存成功的消息
                QtWidgets.QMessageBox.information(
                    self,
                    "保存成功",
                    f"图像已成功保存到:\n{file_path}",
                    QtWidgets.QMessageBox.Ok
                )
            except Exception as e:
                # 显示错误消息
                QtWidgets.QMessageBox.critical(
                    self,
                    "保存失败",
                    f"保存图像时出错:\n{str(e)}",
                    QtWidgets.QMessageBox.Ok
                )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 设置应用程序图标
    icon_path = get_resource_path('image/logo.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = NewtonRingsSimulator()
    window.show()
    sys.exit(app.exec_())