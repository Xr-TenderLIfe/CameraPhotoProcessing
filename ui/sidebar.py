import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QComboBox, \
    QSizePolicy, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt
from logic.file_interchangeably import FolderFilter
import src_rc

# 选项配置
options = QFileDialog.Options()
options |= QFileDialog.DontUseNativeDialog
options |= QFileDialog.ShowDirsOnly  # 只允许选择文件夹

class Sidebar(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 方便调用主窗口方法
        self.path_inputs = {}  # 存储路径和后缀选择框
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        # 创建文件夹选择区域
        self.add_folder_selection(layout, "原始文件夹", "original")
        self.add_folder_selection(layout, "目标文件夹", "target")  # 目标文件夹也需要选择后缀
        self.add_folder_selection(layout, "输出文件夹", "output", has_suffix=False)  # 输出文件夹不需要后缀选择
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)  # 初始值
        self.progress_bar.setFixedHeight(20)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("开始执行")
        self.start_button.setFixedSize(200, 50)
        self. start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(93, 169, 255, 1),
                                            stop:1 rgba(60, 120, 200, 1));
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                color: white;
                font-family: "Microsoft YaHei", "PingFang SC", "Arial";
                padding: 10px;
                border: 2px solid rgba(93, 169, 255, 1);
            }

            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(60, 120, 200, 1),
                                            stop:1 rgba(93, 169, 255, 1));
                border: 2px solid rgba(60, 120, 200, 1);
            }

            QPushButton:pressed {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(40, 90, 150, 1),
                                            stop:1 rgba(30, 80, 140, 1));
                border: 2px solid rgba(30, 80, 140, 1);
            }
        """)
        self.start_button.clicked.connect(self.execute_process)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def add_folder_selection(self, layout, label, key, has_suffix=True):
        """创建文件夹选择行，包含按钮、文本框（显示路径）和可选的后缀选择"""
        folder_layout = QHBoxLayout()

        # 选择文件夹按钮
        folder_button = QPushButton(f"选择{label}")
        folder_button.setFixedSize(150, 40)

        folder_button.clicked.connect(lambda: self.open_folder_dialog(key))
        folder_layout.addWidget(folder_button)

        # 显示路径的文本框
        path_textbox = QLineEdit()
        path_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 允许伸缩
        folder_layout.addWidget(path_textbox)
        self.path_inputs[key] = path_textbox
        if has_suffix:
            suffix_combobox = QComboBox()
            suffix_combobox.setStyleSheet(f"""
                                       QComboBox {{
                                           combobox-popup: 0;
                                           border-style:none;
                                           padding-left:10px;  
                                           width:80px; 
                                           height:30px;
                                           font-size:16px;
                                           font-family:PingFangSC-Regular, PingFang SC;
                                           font-weight:400;
                                           color:rgba(93,169,255,1);
                                           line-height:24px;
                                       }}

                                       QComboBox:drop-down {{
                                           width:40px;
                                           height:30px;
                                           border: none;
                                           subcontrol-position: right center;
                                           subcontrol-origin: padding;
                                       }}

                                       QComboBox:down-arrow {{
                                           border: none;
                                           background: transparent;
                                           image: url(":/commont/image/up.png");
                                       }}

                                       QComboBox:down-arrow:pressed {{
                                           image: url(":/commont/image/up.png");
                                       }}

                                       QComboBox QAbstractItemView {{
                                           color:black;
                                           background: white;
                                           selection-color:rgba(93,169,255,1);
                                           selection-background-color: rgba(200, 200, 200, 1);
                                       }}

                                       QComboBox QAbstractScrollArea QScrollBar:vertical {{
                                           width: 6px;
                                           height: 100px;
                                           background-color: transparent;
                                       }}

                                       QComboBox QAbstractScrollArea QScrollBar::handle:vertical {{
                                           border-radius: 3px;
                                           background: rgba(0,0,0,0.1);
                                       }}

                                       QComboBox QAbstractScrollArea QScrollBar::handle:vertical:hover {{
                                           background: rgb(90, 91, 93);
                                       }}

                                       QComboBox QScrollBar::add-line::vertical {{
                                           border:none;
                                       }}

                                       QComboBox QScrollBar::sub-line::vertical {{
                                           border:none;
                                       }}
                                   """)
            suffix_combobox.setMaxVisibleItems(5)
            suffix_combobox.setObjectName("comboBox")
            suffix_combobox.addItems([".jpg", ".arw",".raw", ".txt", ".png", ".pdf", ".docx"])
            folder_layout.addWidget(suffix_combobox)
            self.path_inputs[f"{key}_suffix"] = suffix_combobox

        layout.addLayout(folder_layout)

    def open_folder_dialog(self, key):
        """使用 QFileDialog 并强制调用系统原生文件选择窗口"""
        folder_name = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            # options=QFileDialog.DontUseNativeDialog  # ✅ 确保使用 **系统原生** 文件选择窗口
        )
        if folder_name:
            self.path_inputs[key].setText(folder_name)

    def execute_process(self):
        """ 执行文件筛选和复制 """
        folder_a = self.path_inputs["original"].text()
        folder_b = self.path_inputs["target"].text()
        folder_c = self.path_inputs["output"].text()

        if not folder_a or not folder_b or not folder_c:
            QMessageBox.warning(self, "错误", "请选择所有文件夹！")
            return

        # 获取选择的后缀
        selected_extension_a = [self.path_inputs["original_suffix"].currentText()]
        selected_extension_b = [self.path_inputs["target_suffix"].currentText()]

        # 创建并启动线程
        self.filter_thread = FolderFilter(folder_a, folder_b, folder_c, selected_extension_a, selected_extension_b)
        self.filter_thread.progress_updated.connect(self.update_progress)  # 连接信号
        self.filter_thread.task_finished.connect(self.on_task_finished)  # 任务完成信号
        self.filter_thread.start()

        self.start_button.setEnabled(False)  # 禁用按钮，防止重复点击
        self.progress_bar.setValue(0)

    def update_progress(self, progress):
        """ 更新进度条 """
        self.progress_bar.setValue(progress)

    def on_task_finished(self):
        """ 任务完成时调用 """
        QMessageBox.information(self, "成功", "文件复制完成！")
        self.start_button.setEnabled(True)  # 重新启用按钮
        self.progress_bar.setValue(100)  # 设置满进度