import locale
import os
import signal
import subprocess
import sys
import threading
from pathlib import Path

from PyQt6.QtCore import QProcess, QTimer, Qt
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)


PRO_STYLESHEET = """
/* 1. 主容器 */
#MainContainer {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

/* 2. 标题栏 */
#TitleBar {
    background-color: transparent;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid #F3F4F6;
}
QLabel#app_title {
    color: #374151;
    font-family: 'Segoe UI', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    padding-left: 8px;
}
QLabel#status_badge {
    color: #9CA3AF;
    font-size: 9pt;
    font-weight: 600;
    padding-right: 8px;
}

/* 3. 窗口控制按钮 */
QPushButton#win_btn {
    background-color: transparent;
    border: none;
    color: #6B7280;
    border-radius: 4px;
    font-size: 12px;
    margin: 4px;
}
QPushButton#win_btn:hover { background-color: #F3F4F6; color: #111827; }
QPushButton#win_btn[variant="close"]:hover { background-color: #EF4444; color: white; }

/* 4. 通用标签 */
QLabel.field_label {
    color: #6B7280;
    font-size: 9pt;
    font-weight: 600;
}

/* 5. 输入控件 */
QLineEdit {
    background-color: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 6px 10px;
    color: #1F2937;
    font-family: 'Consolas', monospace;
    font-size: 10pt;
}
QLineEdit:focus {
    background-color: #FFFFFF;
    border-color: #3B82F6;
}

/* 6. 按钮 */
QPushButton {
    border-radius: 6px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}
QPushButton#action_btn_start {
    background-color: #2563EB;
    color: white;
    border: none;
    padding: 8px 30px;
    font-size: 10pt;
}
QPushButton#action_btn_start:hover { background-color: #1D4ED8; }
QPushButton#action_btn_start:disabled {
    background-color: #93C5FD;
    color: #EFF6FF;
}

/* 7. 日志区域 */
QFrame#LogToolbar {
    background-color: #F9FAFB;
    border-top: 1px solid #E5E7EB;
    border-left: 1px solid #E5E7EB;
    border-right: 1px solid #E5E7EB;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QLabel#log_title {
    color: #6B7280;
    font-weight: bold;
    font-size: 9pt;
    padding-left: 5px;
}
QPushButton#toolbar_clear_btn {
    background-color: transparent;
    color: #6B7280;
    border: none;
    font-size: 9pt;
    padding: 4px 10px;
}
QPushButton#toolbar_clear_btn:hover {
    background-color: #E5E7EB;
    color: #374151;
    border-radius: 4px;
}

QPlainTextEdit {
    background-color: #111827;
    border: 1px solid #E5E7EB;
    border-top: none;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    font-family: 'Consolas', monospace;
    color: #E5E7EB;
    padding: 12px;
    font-size: 9.5pt;
}

/* Console Panel */
QFrame#ConsolePanel {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
}
QFrame#ConsoleHeader {
    background-color: #F9FAFB;
    border-bottom: 1px solid #E5E7EB;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QLabel#console_title {
    color: #6B7280;
    font-weight: 600;
    font-size: 9pt;
    padding-left: 5px;
}
QPushButton#console_clear_btn {
    background-color: transparent;
    color: #6B7280;
    border: none;
    font-size: 9pt;
    padding: 4px 10px;
}
QPushButton#console_clear_btn:hover {
    background-color: #E5E7EB;
    color: #374151;
    border-radius: 4px;
}
QPushButton#console_stop_btn {
    background-color: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FECACA;
    font-size: 9pt;
    padding: 4px 10px;
    border-radius: 6px;
}
QPushButton#console_stop_btn:hover {
    background-color: #FECACA;
}
QPushButton#console_stop_btn:disabled {
    background-color: #F3F4F6;
    color: #9CA3AF;
    border: 1px solid #E5E7EB;
}
QPushButton#console_close_btn {
    background-color: transparent;
    color: #6B7280;
    border: none;
    font-size: 11pt;
    padding: 2px 8px;
}
QPushButton#console_close_btn:hover {
    background-color: #E5E7EB;
    color: #374151;
    border-radius: 6px;
}
QFrame#ConsoleCommandBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
}
QLineEdit#panel_cmd_input {
    margin: 8px 0;
}
QPushButton#panel_run_btn {
    background-color: #2563EB;
    color: white;
    border: none;
    padding: 6px 16px;
    font-size: 9pt;
}
QPushButton#panel_run_btn:hover {
    background-color: #1D4ED8;
}
QPushButton#panel_run_btn:disabled {
    background-color: #93C5FD;
    color: #EFF6FF;
}

/* Pager */
QPushButton#pager_btn {
    background-color: white;
    border: 1px solid #D1D5DB;
    color: #4B5563;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 9pt;
}
QPushButton#pager_btn:disabled {
    color: #9CA3AF;
    border-color: #E5E7EB;
}
QLabel#page_label {
    color: #6B7280;
    font-size: 9pt;
    padding: 0 6px;
}
QLabel#empty_hint {
    color: #9CA3AF;
    font-size: 10pt;
}
"""


# 每次执行都分配一个唯一会话键，避免相同命令互相覆盖。
CommandKey = tuple[int, str, str]


class ConsolePanel(QFrame):
    def __init__(self, title: str, on_stop, on_close, on_run):
        super().__init__()
        self.setObjectName("ConsolePanel")
        self._on_stop = on_stop
        self._on_close = on_close
        self._on_run = on_run
        self._is_running = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("ConsoleHeader")
        header.setFixedHeight(28)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 0, 8, 0)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("console_title")
        self.title_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.title_label.setMinimumWidth(0)
        self.title_label.setToolTip(title)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("console_stop_btn")
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.clicked.connect(self._handle_stop)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setObjectName("console_clear_btn")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("console_close_btn")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self._handle_close)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.stop_btn)
        header_layout.addWidget(self.clear_btn)
        header_layout.addWidget(self.close_btn)

        # 面板内保留一个轻量输入条，命令结束后可直接继续执行下一条。
        self.command_bar = QFrame()
        self.command_bar.setObjectName("ConsoleCommandBar")
        command_layout = QHBoxLayout(self.command_bar)
        command_layout.setContentsMargins(8, 0, 8, 0)
        command_layout.setSpacing(8)

        self.command_input = QLineEdit()
        self.command_input.setObjectName("panel_cmd_input")
        self.command_input.setPlaceholderText("执行完毕后可在这里输入新命令")
        self.command_input.setMinimumWidth(0)
        self.command_input.returnPressed.connect(self._handle_run)
        self.command_input.textChanged.connect(self._update_run_state)

        self.run_btn = QPushButton("执行")
        self.run_btn.setObjectName("panel_run_btn")
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self._handle_run)

        command_layout.addWidget(self.command_input, 1)
        command_layout.addWidget(self.run_btn)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setFrameShape(QFrame.Shape.NoFrame)

        layout.addWidget(header)
        layout.addWidget(self.command_bar)
        layout.addWidget(self.editor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.set_running_state(False)

    def set_title(self, title: str):
        self.title_label.setText(title)
        self.title_label.setToolTip(title)

    def set_command_text(self, text: str):
        self.command_input.setText(text)
        self.command_input.setToolTip(text)

    def command_text(self) -> str:
        return self.command_input.text()

    def set_running_state(self, running: bool):
        self._is_running = running
        self.stop_btn.setEnabled(running)
        self.command_input.setEnabled(not running)
        self._update_run_state()

    def _update_run_state(self):
        can_run = (not self._is_running) and bool(self.command_text().strip())
        self.run_btn.setEnabled(can_run)

    def _handle_stop(self):
        if callable(self._on_stop):
            self._on_stop(self)

    def _handle_close(self):
        if callable(self._on_close):
            self._on_close(self)

    def _handle_run(self):
        text = self.command_text().strip()
        if not text or self._is_running:
            return
        if callable(self._on_run):
            self._on_run(self, text)

    def append_line(self, text: str):
        if not text:
            return
        self.editor.appendPlainText(text)
        self.editor.verticalScrollBar().setValue(self.editor.verticalScrollBar().maximum())

    def clear(self):
        self.editor.clear()


class CommandController(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("托盘执行器")
        self.resize(840, 760)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.old_pos = None
        self.default_work_dir = str(Path.cwd())
        self.output_encoding = locale.getpreferredencoding(False) or "utf-8"
        self.next_command_id = 1
        self.processes: dict[CommandKey, QProcess] = {}
        self.last_pids: dict[CommandKey, int] = {}
        self.console_panels: dict[CommandKey, ConsolePanel] = {}
        self.panel_keys: dict[ConsolePanel, CommandKey] = {}
        self.console_page_index: dict[ConsolePanel, int] = {}
        self.console_pages: list[QWidget] = []
        self.page_layouts: list[QHBoxLayout] = []
        self.page_counts: list[int] = []
        self.page_panels: list[list[ConsolePanel]] = []
        self.empty_page = None

        self._init_ui()
        self._init_tray()
        self._init_defaults()

    def _init_defaults(self):
        self.workdir_input.setText(self.default_work_dir)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_base = QVBoxLayout(central)
        layout_base.setContentsMargins(10, 10, 10, 10)

        self.container = QFrame()
        self.container.setObjectName("MainContainer")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.container.setGraphicsEffect(shadow)

        layout_container = QVBoxLayout(self.container)
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setSpacing(0)

        header = QFrame()
        header.setObjectName("TitleBar")
        header.setFixedHeight(38)
        header.mouseMoveEvent = self.mouseMoveEvent
        header.mousePressEvent = self.mousePressEvent

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 0, 6, 0)

        self.title_label = QLabel("托盘执行器")
        self.title_label.setObjectName("app_title")

        self.status_label = QLabel("● 就绪")
        self.status_label.setObjectName("status_badge")

        btn_min = QPushButton("－")
        btn_min.setObjectName("win_btn")
        btn_min.setFixedSize(28, 28)
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton("✕")
        btn_close.setObjectName("win_btn")
        btn_close.setProperty("variant", "close")
        btn_close.setFixedSize(28, 28)
        btn_close.clicked.connect(self.close)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        header_layout.addWidget(btn_min)
        header_layout.addWidget(btn_close)

        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(20, 20, 20, 10)
        control_layout.setSpacing(10)

        workdir_label = QLabel("工作目录")
        workdir_label.setProperty("class", "field_label")

        self.workdir_input = QLineEdit()
        self.workdir_input.setPlaceholderText("留空则使用当前目录")
        self.workdir_input.setFixedHeight(32)
        self.workdir_input.returnPressed.connect(self.start_command)
        self.workdir_input.textChanged.connect(self._update_action_state)

        command_label = QLabel("命令")
        command_label.setProperty("class", "field_label")

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("例如：python main.py  或  uvicorn app:app --reload")
        self.command_input.setFixedHeight(32)
        self.command_input.returnPressed.connect(self.start_command)
        self.command_input.textChanged.connect(self._update_action_state)

        note_label = QLabel(self._shell_note_text())
        note_label.setProperty("class", "field_label")

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.main_btn = QPushButton("执行命令")
        self.main_btn.setObjectName("action_btn_start")
        self.main_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_btn.clicked.connect(self.start_command)

        action_layout.addWidget(note_label)
        action_layout.addStretch()
        action_layout.addWidget(self.main_btn)

        control_layout.addWidget(workdir_label)
        control_layout.addWidget(self.workdir_input)
        control_layout.addWidget(command_label)
        control_layout.addWidget(self.command_input)
        control_layout.addLayout(action_layout)

        log_wrapper = QWidget()
        log_layout = QVBoxLayout(log_wrapper)
        log_layout.setContentsMargins(20, 0, 20, 20)
        log_layout.setSpacing(0)

        toolbar = QFrame()
        toolbar.setObjectName("LogToolbar")
        toolbar.setFixedHeight(32)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 0, 10, 0)

        lbl_log = QLabel("运行日志 (Console Output)")
        lbl_log.setObjectName("log_title")

        self.prev_page_btn = QPushButton("上一页")
        self.prev_page_btn.setObjectName("pager_btn")
        self.prev_page_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_page_btn.clicked.connect(self._prev_page)

        self.page_label = QLabel("1/1")
        self.page_label.setObjectName("page_label")

        self.next_page_btn = QPushButton("下一页")
        self.next_page_btn.setObjectName("pager_btn")
        self.next_page_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_page_btn.clicked.connect(self._next_page)

        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.setObjectName("toolbar_clear_btn")
        self.clear_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton))
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self._clear_current_page)

        toolbar_layout.addWidget(lbl_log)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.prev_page_btn)
        toolbar_layout.addWidget(self.page_label)
        toolbar_layout.addWidget(self.next_page_btn)
        toolbar_layout.addWidget(self.clear_btn)

        self.console_stack = QStackedWidget()
        self.empty_page = QWidget()
        empty_layout = QVBoxLayout(self.empty_page)
        empty_layout.setContentsMargins(0, 0, 0, 0)
        empty_layout.addStretch()
        empty_label = QLabel("暂无输出")
        empty_label.setObjectName("empty_hint")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_label)
        empty_layout.addStretch()
        self.console_stack.addWidget(self.empty_page)

        log_layout.addWidget(toolbar)
        log_layout.addWidget(self.console_stack)

        layout_container.addWidget(header)
        layout_container.addWidget(control_panel)
        layout_container.addWidget(log_wrapper, 1)

        layout_base.addWidget(self.container)
        self.setStyleSheet(PRO_STYLESHEET)
        self._update_action_state()

    def _init_tray(self):
        QApplication.instance().setQuitOnLastWindowClosed(False)
        self.tray = QSystemTrayIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon), self)
        menu = QMenu()
        menu.addAction("显示主界面", self.showNormal)
        menu.addAction("退出程序", self.exit_app)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda reason: self.showNormal() if reason == QSystemTrayIcon.ActivationReason.Trigger else None
        )
        self.tray.show()

    def _shell_note_text(self) -> str:
        if sys.platform.startswith("win"):
            return "通过系统 shell 执行：cmd.exe /C"
        return "通过系统 shell 执行：sh -lc"

    def _make_key(self, work_dir: str, command: str) -> CommandKey:
        key = (self.next_command_id, work_dir, command)
        self.next_command_id += 1
        return key

    def _key_work_dir(self, key: CommandKey) -> str:
        return key[1]

    def _key_command(self, key: CommandKey) -> str:
        return key[2]

    def _format_target(self, key: CommandKey) -> str:
        work_dir = self._key_work_dir(key)
        command = self._key_command(key)
        compact = " ".join(command.split())
        preview = compact if len(compact) <= 56 else f"{compact[:53]}..."
        return f"{preview} @ {work_dir}"

    def _ensure_pages_ready(self):
        if self.empty_page is None:
            return
        self.console_stack.removeWidget(self.empty_page)
        self.empty_page.deleteLater()
        self.empty_page = None

    def _restore_empty_page(self):
        if self.empty_page is not None:
            return
        self.empty_page = QWidget()
        empty_layout = QVBoxLayout(self.empty_page)
        empty_layout.setContentsMargins(0, 0, 0, 0)
        empty_layout.addStretch()
        empty_label = QLabel("暂无输出")
        empty_label.setObjectName("empty_hint")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_label)
        empty_layout.addStretch()
        self.console_stack.addWidget(self.empty_page)
        self.console_stack.setCurrentWidget(self.empty_page)

    def _create_page(self) -> int:
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        self.console_pages.append(page)
        self.page_layouts.append(layout)
        self.page_counts.append(0)
        self.page_panels.append([])
        self.console_stack.addWidget(page)
        return len(self.console_pages) - 1

    def _rebalance_page(self, page_index: int):
        if page_index < 0 or page_index >= len(self.page_layouts):
            return
        layout = self.page_layouts[page_index]
        # 同一页最多两个面板，始终强制 1:1 均分宽度。
        for index, panel in enumerate(self.page_panels[page_index]):
            layout.setStretch(index, 1)
            layout.setStretchFactor(panel, 1)
            panel.setMinimumWidth(0)

    def _set_page(self, index: int):
        if index < 0 or index >= self.console_stack.count():
            return
        self.console_stack.setCurrentIndex(index)
        self._update_pager()

    def _update_pager(self):
        total = max(1, self.console_stack.count())
        current = self.console_stack.currentIndex() + 1
        self.page_label.setText(f"{current}/{total}")
        self.prev_page_btn.setEnabled(current > 1)
        self.next_page_btn.setEnabled(current < total)

    def _prev_page(self):
        self._set_page(self.console_stack.currentIndex() - 1)

    def _next_page(self):
        self._set_page(self.console_stack.currentIndex() + 1)

    def _clear_current_page(self):
        if self.empty_page is not None:
            return
        index = self.console_stack.currentIndex()
        if index < 0 or index >= len(self.page_panels):
            return
        for panel in self.page_panels[index]:
            panel.clear()

    def _add_console_panel(self, key: CommandKey) -> ConsolePanel:
        self._ensure_pages_ready()
        if not self.page_counts or self.page_counts[-1] >= 2:
            page_index = self._create_page()
        else:
            page_index = len(self.page_counts) - 1

        panel = ConsolePanel(
            self._format_target(key),
            self._stop_panel,
            self._close_console,
            self._run_from_panel,
        )
        panel.set_command_text(self._key_command(key))
        self.console_panels[key] = panel
        self.panel_keys[panel] = key
        self.console_page_index[panel] = page_index
        self.page_layouts[page_index].insertWidget(self.page_counts[page_index], panel, 1)
        self.page_counts[page_index] += 1
        self.page_panels[page_index].append(panel)
        self._rebalance_page(page_index)
        self._set_page(page_index)
        return panel

    def _get_console(self, key: CommandKey, create: bool = True):
        panel = self.console_panels.get(key)
        if panel is None and create:
            panel = self._add_console_panel(key)
        return panel

    def _ensure_console(self, key: CommandKey):
        return self._get_console(key, create=True)

    def _focus_console(self, key: CommandKey):
        panel = self.console_panels.get(key)
        if panel is None:
            return
        page_index = self.console_page_index.get(panel)
        if page_index is not None:
            self._set_page(page_index)

    def _stop_panel(self, panel: ConsolePanel):
        key = self.panel_keys.get(panel)
        if key is not None:
            self.stop_command(key)

    def _run_from_panel(self, panel: ConsolePanel, command: str):
        key = self.panel_keys.get(panel)
        if key is None:
            return
        work_dir = self._key_work_dir(key)
        self._start_command(command, work_dir, panel=panel)

    def _remap_panel_key(self, panel: ConsolePanel, new_key: CommandKey) -> bool:
        old_key = self.panel_keys.get(panel)
        if old_key is not None and old_key != new_key:
            self.console_panels.pop(old_key, None)
            self.processes.pop(old_key, None)
            self.last_pids.pop(old_key, None)

        self.console_panels[new_key] = panel
        self.panel_keys[panel] = new_key
        panel.set_command_text(self._key_command(new_key))
        return old_key != new_key

    def _close_console(self, panel: ConsolePanel):
        key = self.panel_keys.get(panel)
        if key in self.processes and self._is_key_running(key):
            self.stop_command(key)
        if key is not None:
            self.console_panels.pop(key, None)
        self.panel_keys.pop(panel, None)
        page_index = self.console_page_index.pop(panel, None)
        if page_index is None:
            return

        layout = self.page_layouts[page_index]
        layout.removeWidget(panel)
        panel.setParent(None)
        panel.deleteLater()
        self.page_counts[page_index] = max(0, self.page_counts[page_index] - 1)
        if panel in self.page_panels[page_index]:
            self.page_panels[page_index].remove(panel)
        self._rebalance_page(page_index)

        if self.page_counts[page_index] == 0:
            page = self.console_pages.pop(page_index)
            self.page_layouts.pop(page_index)
            self.page_counts.pop(page_index)
            self.page_panels.pop(page_index)
            self.console_stack.removeWidget(page)
            page.deleteLater()

            for mapped_panel, idx in list(self.console_page_index.items()):
                if idx > page_index:
                    self.console_page_index[mapped_panel] = idx - 1

        if not self.console_pages:
            self._restore_empty_page()
        self._update_pager()

    def _is_key_running(self, key: CommandKey) -> bool:
        proc = self.processes.get(key)
        if not proc:
            return False
        if proc.state() == QProcess.ProcessState.Running:
            return True
        self.processes.pop(key, None)
        return False

    def _running_count(self) -> int:
        running = 0
        for key, proc in list(self.processes.items()):
            if proc.state() == QProcess.ProcessState.Running:
                running += 1
            else:
                self.processes.pop(key, None)
                console = self.console_panels.get(key)
                if console:
                    console.set_running_state(False)
        return running

    def _set_main_button(self):
        self.main_btn.setText("执行命令")
        self.main_btn.setObjectName("action_btn_start")
        self.main_btn.setStyle(self.main_btn.style())

    def _update_action_state(self):
        count = self._running_count()
        if count > 0:
            label = f"● 运行中 ({count})" if count > 1 else "● 运行中"
            self.status_label.setText(label)
            self.status_label.setStyleSheet("color: #10B981; font-weight: bold; padding-right: 8px;")
        else:
            self.status_label.setText("● 就绪")
            self.status_label.setStyleSheet("color: #9CA3AF; font-weight: bold; padding-right: 8px;")

        self._set_main_button()
        self.main_btn.setEnabled(bool(self.command_input.text().strip()))
        self._update_pager()

    def _append_message(self, key: CommandKey, text: str):
        panel = self._get_console(key, create=False)
        if panel is None:
            return
        panel.append_line(text)

    def _notify_error(self, message: str):
        QMessageBox.information(self, "提示", message)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.old_pos = None

    def _normalized_work_dir(self) -> str | None:
        raw = self.workdir_input.text().strip() or self.default_work_dir
        expanded = os.path.expandvars(raw)
        try:
            path = Path(expanded).expanduser().resolve()
        except (OSError, RuntimeError):
            self._notify_error("工作目录无效。")
            return None
        if not path.exists():
            self._notify_error("工作目录不存在。")
            return None
        if not path.is_dir():
            self._notify_error("工作目录不是文件夹。")
            return None
        return str(path)

    def _build_shell_command(self, command: str) -> tuple[str, list[str]]:
        if sys.platform.startswith("win"):
            shell = os.environ.get("COMSPEC", "cmd.exe")
            return shell, ["/C", command]
        shell = os.environ.get("SHELL", "/bin/sh")
        return shell, ["-lc", command]

    def is_running(self) -> bool:
        return self._running_count() > 0

    def start_command(self):
        command = self.command_input.text().strip()
        if not command:
            self._notify_error("请输入要执行的命令。")
            return

        work_dir = self._normalized_work_dir()
        if work_dir is None:
            return

        self._start_command(command, work_dir)

    def _start_command(self, command: str, work_dir: str, panel: ConsolePanel | None = None):
        key = self._make_key(work_dir, command)

        if panel is None:
            panel = self._add_console_panel(key)
        else:
            # 复用已完成面板时，把面板映射切到新的会话键。
            self._remap_panel_key(panel, key)
            if panel.editor.toPlainText().strip():
                panel.append_line("-" * 60)

        program, args = self._build_shell_command(command)
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.started.connect(lambda key=key, proc=process: self.on_started(key, proc))
        process.finished.connect(
            lambda exit_code, exit_status, key=key, proc=process: self.on_finished(key, proc, exit_code, exit_status)
        )
        process.readyReadStandardOutput.connect(lambda proc=process, key=key: self.on_output(proc, key))
        process.errorOccurred.connect(lambda _err, key=key, proc=process: self.on_error(key, proc))

        self.processes[key] = process
        process.setWorkingDirectory(work_dir)
        panel.set_running_state(True)
        panel.set_title(f"{self._format_target(key)} (启动中)")
        panel.set_command_text(command)
        self._append_message(key, f">> 工作目录: {work_dir}")
        self._append_message(key, f">> 执行命令: {command}")
        process.start(program, args)
        self._focus_console(key)
        self._update_action_state()

    def stop_command(self, key=None):
        if key is None:
            if not self.processes:
                return
            for mapped_key, proc in list(self.processes.items()):
                self._stop_process(mapped_key, proc)
            return

        proc = self.processes.get(key)
        if not proc:
            return
        self._stop_process(key, proc)

    def _stop_process(self, key: CommandKey, proc: QProcess):
        if proc.state() != QProcess.ProcessState.Running:
            return
        pid = proc.processId() or self.last_pids.get(key, 0)
        if pid:
            self.last_pids[key] = pid
        proc.terminate()
        if pid:
            self._kill_process_tree(pid, force=False, key=key)
            QTimer.singleShot(1500, lambda p=pid, k=key: self._kill_process_tree(p, force=True, key=k))
        QTimer.singleShot(2000, proc.kill)
        self._append_message(key, f">> 正在停止命令: {self._format_target(key)}")

    def _kill_process_tree(self, pid: int, force: bool, key=None):
        if not pid:
            return
        # 停止主进程时顺带清理它派生出来的子进程，避免后台残留。
        if sys.platform.startswith("win"):
            cmd = ["taskkill", "/PID", str(pid), "/T"]
            if force:
                cmd.append("/F")
            self._run_kill_command_async(cmd, key)
            return

        sig = signal.SIGKILL if force else signal.SIGTERM
        self._run_kill_command_async(["pkill", f"-{sig.name}", "-P", str(pid)], key)
        try:
            os.kill(pid, sig)
        except ProcessLookupError:
            return

    def _run_kill_command_async(self, cmd: list[str], key=None):
        def _worker():
            try:
                kwargs = {
                    "stdout": subprocess.DEVNULL,
                    "stderr": subprocess.DEVNULL,
                }
                if sys.platform.startswith("win") and hasattr(subprocess, "CREATE_NO_WINDOW"):
                    kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                result = subprocess.run(cmd, **kwargs)
                if result.returncode != 0:
                    message = f">> 结束进程失败: {' '.join(cmd)}"
                    if key:
                        QTimer.singleShot(0, lambda text=message, target=key: self._append_message(target, text))
                    else:
                        QTimer.singleShot(0, lambda text=message: self._notify_error(text))
            except FileNotFoundError:
                message = f">> 未找到命令: {cmd[0]}"
                if key:
                    QTimer.singleShot(0, lambda text=message, target=key: self._append_message(target, text))
                else:
                    QTimer.singleShot(0, lambda text=message: self._notify_error(text))

        threading.Thread(target=_worker, daemon=True).start()

    def on_started(self, key: CommandKey, proc: QProcess):
        pid = proc.processId()
        if pid:
            self.last_pids[key] = pid
        console = self._get_console(key, create=False)
        if console:
            console.set_running_state(True)
            console.set_command_text(self._key_command(key))
            console.set_title(f"{self._format_target(key)} (运行中)")
        self._update_action_state()

    def on_finished(self, key: CommandKey, proc: QProcess, exit_code: int, exit_status: QProcess.ExitStatus):
        self.processes.pop(key, None)
        self.last_pids.pop(key, None)
        console = self.console_panels.get(key)
        if console:
            label = "崩溃退出" if exit_status == QProcess.ExitStatus.CrashExit else "已退出"
            console.append_line(f">> {label} (code={exit_code})")
            console.set_running_state(False)
            console.set_title(f"{self._format_target(key)} (已停止)")
        self._update_action_state()

    def on_error(self, key: CommandKey, proc: QProcess):
        error_text = proc.errorString().strip()
        if error_text:
            self._append_message(key, f">> 启动错误: {error_text}")
        if proc.state() != QProcess.ProcessState.Running:
            console = self.console_panels.get(key)
            if console:
                console.set_running_state(False)
        self._update_action_state()

    def on_output(self, proc: QProcess, key: CommandKey):
        data = proc.readAllStandardOutput().data()
        if not data:
            return
        try:
            text = data.decode(self.output_encoding, "ignore")
        except LookupError:
            text = data.decode("utf-8", "ignore")
        if not text:
            text = data.decode("utf-8", "ignore")
        console = self._get_console(key, create=False)
        if console:
            for line in text.rstrip().splitlines():
                console.append_line(line)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage("托盘执行器", "已最小化到托盘", QSystemTrayIcon.MessageIcon.Information, 1000)

    def exit_app(self):
        if self.is_running():
            for key, proc in list(self.processes.items()):
                pid = proc.processId() or self.last_pids.get(key, 0)
                if pid:
                    self.last_pids[key] = pid
                    self._kill_process_tree(pid, force=True, key=key)
                proc.terminate()
                proc.waitForFinished(2000)
                if proc.state() == QProcess.ProcessState.Running:
                    proc.kill()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CommandController()
    win.show()
    sys.exit(app.exec())
