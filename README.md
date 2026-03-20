# Win_cmd_托盘执行器 / Win_cmd_TrayExec

## 简介 / Overview

中文：

`CMDS_cn.py` 和 `CMDS_en.py` 是这个工具的源码文件。

- 中文程序显示名：`托盘执行器`
- 英文程序显示名：`TrayExec`

这是一个托盘常驻的图形化命令执行器。你可以直接在 GUI 中输入命令、执行命令，并查看输出，不需要手动打开终端窗口。

English:

`CMDS_cn.py` and `CMDS_en.py` are the source files for this tool.

- Chinese app name: `托盘执行器`
- English app name: `TrayExec`

This is a tray-resident graphical command runner. You can enter commands, run them, and view the output directly from the GUI without manually opening a terminal.

## 运行前需要 / Requirements

中文：

先安装 `PyQt6`：

```bash
pip install PyQt6
```

English:

Install `PyQt6` first:

```bash
pip install PyQt6
```

## 启动方式 / How To Start

中文：

运行中文版源码：

```bash
python CMDS_cn.py
```

运行英文版源码：

```bash
python CMDS_en.py
```

English:

Run the Chinese source:

```bash
python CMDS_cn.py
```

Run the English source:

```bash
python CMDS_en.py
```

## 使用方法 / How To Use

中文：

1. 在 `工作目录` 中填写命令要执行的目录
2. 在 `命令` 中输入要执行的命令
3. 点击 `执行命令`

示例：

```bash
python main.py
```

或：

```bash
uvicorn app:app --reload
```

English:

1. Enter the target folder in `Working Directory`
2. Enter the command in `Command`
3. Click `Run Command`

Examples:

```bash
python main.py
```

or:

```bash
uvicorn app:app --reload
```

## 运行行为 / Runtime Behavior

中文：

- 每次执行命令都会新开一个输出窗口
- 相同命令重复执行，也会新开窗口
- 每页最多显示两个窗口
- 同一页的两个窗口始终均分宽度
- 命令执行结束后，`停止` 按钮会变灰
- 命令执行结束后，可以直接在该窗口里输入下一条命令继续执行

English:

- Every execution opens a new output panel
- Running the same command again also opens a new panel
- Each page shows up to two panels
- Two panels on the same page always split the width evenly
- After a command finishes, the `Stop` button becomes disabled
- After a command finishes, you can enter a new command directly in that panel

## 关闭行为 / Closing Behavior

中文：

点击右上角关闭按钮后，程序会最小化到系统托盘，不会直接退出。

如果要完全退出，请在托盘菜单里选择 `退出程序`。

English:

Clicking the top-right close button minimizes the app to the system tray instead of exiting.

To fully quit, use `Exit` from the tray menu.

## 常见问题 / Common Issues

### 1. 点击执行没有反应 / Nothing Happens After Clicking Run

中文：

先检查命令本身能不能在系统终端里正常运行。

English:

First check whether the command itself works correctly in your normal system terminal.

### 2. 工作目录报错 / Working Directory Error

中文：

请确认：

- 路径存在
- 路径是文件夹
- 当前用户有访问权限

English:

Make sure:

- the path exists
- the path is a folder
- your current user has permission to access it

## PyInstaller 简易打包 / Simple PyInstaller Packaging

中文：

先安装：

```bash
pip install pyinstaller PyQt6
```

中文版建议输出名：

```text
Win_cmd_托盘执行器
```

中文版正式版：

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name Win_cmd_托盘执行器 CMDS_cn.py
```

中文版调试版：

```bash
pyinstaller --noconfirm --clean --onefile --console --name Win_cmd_托盘执行器_debug CMDS_cn.py
```

英文版建议输出名：

```text
Win_cmd_TrayExec
```

英文版正式版：

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name Win_cmd_TrayExec CMDS_en.py
```

英文版调试版：

```bash
pyinstaller --noconfirm --clean --onefile --console --name Win_cmd_TrayExec_debug CMDS_en.py
```

English:

Install the build tools first:

```bash
pip install pyinstaller PyQt6
```

Recommended output name for the Chinese build:

```text
Win_cmd_托盘执行器
```

Chinese release build:

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name Win_cmd_托盘执行器 CMDS_cn.py
```

Chinese debug build:

```bash
pyinstaller --noconfirm --clean --onefile --console --name Win_cmd_托盘执行器_debug CMDS_cn.py
```

Recommended output name for the English build:

```text
Win_cmd_TrayExec
```

English release build:

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name Win_cmd_TrayExec CMDS_en.py
```

English debug build:

```bash
pyinstaller --noconfirm --clean --onefile --console --name Win_cmd_TrayExec_debug CMDS_en.py
```

打包输出目录 / Output Directory:

```text
dist/
```
