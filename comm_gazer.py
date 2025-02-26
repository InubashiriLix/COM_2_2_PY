#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import threading
from blessed import Terminal
import serial.tools.list_ports

# 保存所有曾经出现过的端口，格式： {port: active_status}
seen_ports = {}

# 日志列表，最新日志显示在右侧框中
logs = []
max_logs = 100  # 最多保存日志条数

term = Terminal()


def get_current_ports():
    """获取当前活动的COM口（端口名称集合）"""
    ports = serial.tools.list_ports.comports()
    return set(port.device for port in ports)


def add_log(msg):
    """记录日志，添加时间戳"""
    timestamp = time.strftime("%H:%M:%S")
    logs.append(f"[{timestamp}] {msg}")
    if len(logs) > max_logs:
        logs.pop(0)


def draw_screen(highlight_port=None, flash=False):
    """绘制GUI界面，左侧显示COM口列表，右侧显示日志"""
    with term.location():
        sys.stdout.write(term.home + term.clear)
        left_width = term.width // 2 - 1
        right_width = term.width - left_width - 2

        # 左侧标题及COM口列表
        sys.stdout.write(term.move(0, 0) + term.bold("COM Ports:"))
        row = 1
        for port, active in seen_ports.items():
            # 若当前端口需要高亮且处于闪烁阶段，使用反色显示
            style = term.reverse if (port == highlight_port and flash) else term.normal
            status = "Active" if active else "Inactive"
            line = f"{port:<15} - {status}"
            sys.stdout.write(term.move(row, 0) + style + line + term.normal)
            row += 1

        # 右侧标题及日志显示
        sys.stdout.write(term.move(0, left_width + 2) + term.bold("Logs:"))
        log_start = max(0, len(logs) - term.height + 2)
        for i, line in enumerate(logs[log_start:]):
            sys.stdout.write(term.move(i + 1, left_width + 2) + line[:right_width])
        sys.stdout.flush()


def flash_port(port):
    """对指定端口行进行高亮闪烁3次"""
    for _ in range(3):
        draw_screen(highlight_port=port, flash=True)
        time.sleep(0.2)
        draw_screen(highlight_port=port, flash=False)
        time.sleep(0.2)


def monitor_ports():
    """
    后台线程：
    1. 初始扫描时记录当前设备，不触发高亮闪烁。
    2. 后续每次检测：若检测到新的插入（包括之前拔出后再插入的设备）或拔出事件，
       都将更新状态、记录日志，并对变化的端口进行高亮闪烁提示。
    """
    # 初始扫描，不触发闪烁提示
    initial_ports = get_current_ports()
    for port in initial_ports:
        seen_ports[port] = True
    draw_screen()
    time.sleep(1)

    while True:
        current_ports = get_current_ports()
        changes = []  # 保存本次检测的变化 [(port, event), ...]

        # 检测新插入的设备或拔出后再插入的设备
        for port in current_ports:
            if port not in seen_ports:
                seen_ports[port] = True
                changes.append((port, "inserted"))
                add_log(f"{port} inserted")
            elif seen_ports[port] is False:
                seen_ports[port] = True
                changes.append((port, "inserted"))
                add_log(f"{port} inserted")

        # 检测拔出事件：之前为Active但当前不在检测到的设备中
        for port in list(seen_ports.keys()):
            if seen_ports[port] and port not in current_ports:
                seen_ports[port] = False
                changes.append((port, "removed"))
                add_log(f"{port} removed")

        # 对每个变化的端口进行闪烁高亮提示
        for port, event in changes:
            flash_port(port)
        draw_screen()
        time.sleep(1)


def main():
    # 使用 fullscreen 模式和 cbreak 模式
    with term.fullscreen(), term.cbreak():
        draw_screen()
        t = threading.Thread(target=monitor_ports, daemon=True)
        t.start()
        # 按 'q' 键退出程序
        while True:
            inp = term.inkey(timeout=0.5)
            if inp.lower() == "q":
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
