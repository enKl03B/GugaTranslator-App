import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel, QMessageBox, QDialog, QTabWidget
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import QEvent, QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import pyperclip
import darkdetect
from guga_translator import encode, decode

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(450, 280)

        main_layout = QVBoxLayout(self)
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # --- About Tab ---
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel()
        pixmap = QPixmap(resource_path('res/icon.png')).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        about_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        about_layout.addSpacing(10)

        title_label = QLabel("🐧 企鹅语转换工具")
        title_font = self.font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        about_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("<i>好像成为人类啊</i>")
        subtitle_font = self.font()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        about_layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        about_layout.addStretch()

        version_label = QLabel("Ver:1.0.0")
        version_font = self.font()
        version_font.setPointSize(9)
        version_label.setFont(version_font)
        about_layout.addWidget(version_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        about_tab.setLayout(about_layout)

        # --- Acknowledgements Tab ---
        ack_tab = QWidget()
        ack_layout = QVBoxLayout(ack_tab)
        
        ack_text = QLabel()
        ack_text.setTextFormat(Qt.TextFormat.RichText)
        ack_text.setOpenExternalLinks(True)
        ack_text.setWordWrap(True)
        ack_text.setText("""
            <h3>致谢</h3>
            <ul>
                <li>"gugugaga"音频来自B站，原视频链接：<a href="https://www.bilibili.com/video/BV1ewwxesEu4">https://www.bilibili.com/video/BV1ewwxesEu4</a></li>
                <br>
                <li>代码由豆包/Gemini2.5系列大模型完成</li>
                <br>
                <li>企鹅图标来源网络</li>
            </ul>
        """)
        ack_layout.addWidget(ack_text)
        ack_layout.addStretch()
        ack_tab.setLayout(ack_layout)

        tab_widget.addTab(about_tab, "关于")
        tab_widget.addTab(ack_tab, "致谢")

class GugaTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('res/icon.png')))
        self.setWindowTitle("🐧 企鹅语转换工具")
        self.setGeometry(100, 100, 600, 550)
        
        self.penguin_click_count = 0
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(resource_path('res/gugugaga.mp3')))
        
        self._define_themes()
        self.sync_theme_with_system()
        
        self.init_ui()
        self.apply_theme()

    def changeEvent(self, event):
        """Listen for system theme changes."""
        if event.type() == QEvent.Type.ApplicationPaletteChange:
            self.sync_theme_with_system()
        super().changeEvent(event)

    def sync_theme_with_system(self):
        """Detect system theme and apply it."""
        theme_name = darkdetect.theme()
        if theme_name:
            self.current_theme = 'dark' if theme_name == 'Dark' else 'light'
        else:
            self.current_theme = 'light'
        
        if hasattr(self, 'theme_btn'):
            self.apply_theme()

    def _define_themes(self):
        self.light_theme = {
            "bg": "#f0f0f0", "text": "#000000", "input_bg": "#ffffff", "border": "#cccccc",
            "btn_encode_bg": "#3b82f6", "btn_encode_hover": "#3473db",
            "btn_decode_bg": "#6366f1", "btn_decode_hover": "#5254c1",
            "btn_swap_bg": "#6b7280", "btn_swap_hover": "#5a6069",
            "btn_other_border": "#cccccc", "btn_other_bg_hover": "#e0e0e0", "btn_other_text": "#555555"
        }
        self.dark_theme = {
            "bg": "#2d3748", "text": "#e2e8f0", "input_bg": "#1a202c", "border": "#4a5568",
            "btn_encode_bg": "#3b82f6", "btn_encode_hover": "#4a90e2",
            "btn_decode_bg": "#6366f1", "btn_decode_hover": "#7b7de8",
            "btn_swap_bg": "#a0aec0", "btn_swap_hover": "#718096",
            "btn_other_border": "#4a5568", "btn_other_bg_hover": "#4a5568", "btn_other_text": "#e2e8f0"
        }

    def init_ui(self):
        # Menu Bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("文件")
        about_action = file_menu.addAction("关于")
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("退出")
        exit_action.triggered.connect(self.close)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        input_header_layout = QHBoxLayout()
        input_label = QLabel("输入文本:")
        
        self.penguin_btn = QPushButton("🐧")
        self.penguin_btn.setObjectName("penguinBtn")
        self.penguin_btn.setFixedWidth(40)
        self.penguin_btn.clicked.connect(self.handle_penguin_click)

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setFixedWidth(40)
        self.theme_btn.clicked.connect(self.toggle_theme)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setFixedWidth(60)
        self.clear_btn.clicked.connect(self.clear_text)
        
        input_header_layout.addWidget(input_label)
        input_header_layout.addStretch()
        input_header_layout.addWidget(self.penguin_btn)
        input_header_layout.addWidget(self.theme_btn)
        input_header_layout.addWidget(self.clear_btn)
        
        self.input_text = QTextEdit()
        main_layout.addLayout(input_header_layout)
        main_layout.addWidget(self.input_text, 1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.encode_btn = QPushButton("编码")
        self.encode_btn.setObjectName("encodeBtn")
        self.encode_btn.clicked.connect(self.encode_text)
        self.decode_btn = QPushButton("解码")
        self.decode_btn.setObjectName("decodeBtn")
        self.decode_btn.clicked.connect(self.decode_text)
        self.swap_btn = QPushButton("交换")
        self.swap_btn.setObjectName("swapBtn")
        self.swap_btn.clicked.connect(self.swap_text)
        button_layout.addWidget(self.encode_btn)
        button_layout.addWidget(self.decode_btn)
        button_layout.addWidget(self.swap_btn)
        main_layout.addLayout(button_layout)

        output_header_layout = QHBoxLayout()
        output_label = QLabel("转换结果:")
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.setFixedWidth(60)
        self.copy_btn.clicked.connect(self.copy_output)
        output_header_layout.addWidget(output_label)
        output_header_layout.addStretch()
        output_header_layout.addWidget(self.copy_btn)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addLayout(output_header_layout)
        main_layout.addWidget(self.output_text, 1)

    def apply_theme(self):
        theme = self.light_theme if self.current_theme == 'light' else self.dark_theme
        
        # Apply to menu bar as well
        menu_bar_style = f"QMenuBar {{ background-color: {theme['bg']}; color: {theme['text']}; }}"
        menu_style = f"QMenu {{ background-color: {theme['input_bg']}; color: {theme['text']}; }}"
        
        stylesheet = f"""
            {menu_bar_style}
            {menu_style}
            QWidget {{ background-color: {theme['bg']}; color: {theme['text']}; }}
            QMainWindow {{ background-color: {theme['bg']}; }}
            QLabel {{ color: {theme['text']}; font-size: 14px; background-color: transparent; }}
            QTextEdit {{
                background-color: {theme['input_bg']};
                color: {theme['text']};
                font-size: 13px;
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton {{
                font-size: 13px;
                font-weight: bold;
                color: white;
                border-radius: 4px;
                padding: 8px 12px;
                border: none;
            }}
            QPushButton#encodeBtn {{ background-color: {theme['btn_encode_bg']}; }}
            QPushButton#encodeBtn:hover {{ background-color: {theme['btn_encode_hover']}; }}
            QPushButton#decodeBtn {{ background-color: {theme['btn_decode_bg']}; }}
            QPushButton#decodeBtn:hover {{ background-color: {theme['btn_decode_hover']}; }}
            QPushButton#swapBtn {{ background-color: {theme['btn_swap_bg']}; }}
            QPushButton#swapBtn:hover {{ background-color: {theme['btn_swap_hover']}; }}
            QPushButton#clearBtn, QPushButton#copyBtn, QPushButton#themeBtn, QPushButton#penguinBtn {{
                font-weight: normal;
                color: {theme['btn_other_text']};
                background-color: transparent;
                border: 1px solid {theme['btn_other_border']};
            }}
            QPushButton#clearBtn:hover, QPushButton#copyBtn:hover, QPushButton#themeBtn:hover, QPushButton#penguinBtn:hover {{
                background-color: {theme['btn_other_bg_hover']};
            }}
        """
        self.setStyleSheet(stylesheet)
        
        if self.current_theme == 'light':
            self.theme_btn.setText("🌙")
        else:
            self.theme_btn.setText("☀️")

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def encode_text(self):
        input_str = self.input_text.toPlainText().strip()
        if not input_str:
            self.show_message("警告", "请输入要编码的文本。")
            return
        try:
            result = encode(input_str)
            self.output_text.setText(result)
        except Exception as e:
            self.show_message("编码错误", f"发生错误: {e}", "error")

    def decode_text(self):
        input_str = self.input_text.toPlainText().strip()
        if not input_str:
            self.show_message("警告", "请输入要解码的文本。")
            return
        try:
            result = decode(input_str)
            self.output_text.setText(result)
        except ValueError as e:
            self.show_message("解码错误", f"发生错误: {e}", "error")

    def swap_text(self):
        input_content = self.input_text.toPlainText()
        output_content = self.output_text.toPlainText()
        self.input_text.setText(output_content)
        self.output_text.setText(input_content)

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()

    def copy_output(self):
        output_content = self.output_text.toPlainText().strip()
        if output_content:
            pyperclip.copy(output_content)
            self.show_message("成功", "结果已复制到剪贴板！", "info")
        else:
            self.show_message("警告", "没有内容可以复制。")
    
    def handle_penguin_click(self):
        self.penguin_click_count += 1
        if self.penguin_click_count >= 3:
            if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                self.player.setPosition(0)
            else:
                self.player.play()
            self.penguin_click_count = 0

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def show_message(self, title, message, level="warning"):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if level == "info":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif level == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        else:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GugaTranslatorApp()
    window.show()
    sys.exit(app.exec()) 