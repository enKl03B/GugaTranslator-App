
<p align="center">
  <img src="./res/icon.png" alt="企鹅语转换工具图标">
</p>


<p align="center">
  <h1>🐧 企鹅语转换工具 - 应用端</h1>
</p>

<p align="center"><em>好想成为人类啊</em></p>

## 项目简介

这是一个将普通文本转换为“企鹅语”（一种自定义的 Base64 编码）并能将其解码回普通文本的桌面应用程序。

“企鹅语”的编码规则基于标准 Base64，但使用独特的字符集：“咕”、“嘎”、“🐧”、“🍄”、“哇擦”及其组合来表示 Base64 符号。

具体原理请参考[处理逻辑详解](./LOGIC.md)


## ✨ 功能特性

*   **文本编码/解码**：实现“企鹅语”与普通文本之间的双向转换。
*   **现代GUI界面**：使用 PyQt6 构建，提供美观且响应迅速的用户界面。

# 使用

## 🚀 快速开始 
- 网页端  
    源码在[GugaTrans](https://github.com/enKl03B/GugaTrans)  
    https://guga.078465.xyz/

- 应用端
    1.  前往[Releases](https://github.com/enKl03B/GugaTranslator-App/releases),下载对应系统的软件包
    2. 直接运行或安装即可使用。

## 🛠️ 开发与构建 

如果您想对本项目进行修改或二次开发，请按照以下步骤操作。

<details>
<summary>点击查看操作方式</summary>

### 1. 环境设置

**克隆仓库**
如果您从 Git 仓库获取代码，请先克隆它：
```bash
git clone https://github.com/enKl03B/GugaTranslator-App.git
cd GugaTrans-App
```
(如果已经下载了项目文件，请跳过此步骤)

**创建并激活虚拟环境**
强烈建议使用虚拟环境来管理项目依赖。
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

**安装依赖**
激活虚拟环境后，安装 `requirements.txt` 文件中列出的所有依赖项：
```bash
pip install -r requirements.txt
```

### 2. 运行应用

在激活虚拟环境的情况下，从项目根目录运行 `main_gui.py` 文件：
```bash
python main_gui.py
```

### 3. 打包应用

如果您想将应用打包成一个独立的可执行文件，请运行以下命令：
```bash
pyinstaller --onefile --windowed --name GugaTranslator --icon="res/icon.png" --add-data="res;res" main_gui.py
```
打包成功后，可执行文件会生成在 `dist` 文件夹中。

</details>

## 🔧 技术栈

*   **Python**: 主要编程语言。
*   **PyQt6**: 用于构建图形用户界面。
*   **pyperclip**: 用于实现剪贴板“复制”功能。
*   **darkdetect**: 用于检测系统深色/浅色模式。
*   **PyInstaller**: 用于将应用打包成可执行文件。
*   **Pillow**: 在打包过程中自动处理图标格式转换。

## 📂 文件结构

```
GugaTrans-App/
  ├── res/                 # 存放资源文件
  │   ├── icon.png         # 应用程序图标
  │   └── gugugaga.mp3     # 彩蛋音频
  ├── guga_translator.py   # 核心编码/解码逻辑
  ├── main_gui.py          # PyQt6 GUI 应用程序主文件
  └──  requirements.txt     # 项目依赖列表
```


## 📃 许可证
GPL-3.0