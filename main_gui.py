import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QEvent
import pyperclip
import darkdetect
from guga_translator import encode, decode

class GugaTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("企鹅语转换工具")
        self.setGeometry(100, 100, 600, 550)
        
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
        self.current_theme = 'dark' if theme_name == 'Dark' else 'light'
        if hasattr(self, 'theme_btn'): # Check if UI is initialized
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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        input_header_layout = QHBoxLayout()
        input_label = QLabel("输入文本:")
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
        stylesheet = f"""
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
            QPushButton#clearBtn, QPushButton#copyBtn, QPushButton#themeBtn {{
                font-weight: normal;
                color: {theme['btn_other_text']};
                background-color: transparent;
                border: 1px solid {theme['btn_other_border']};
            }}
            QPushButton#clearBtn:hover, QPushButton#copyBtn:hover, QPushButton#themeBtn:hover {{
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