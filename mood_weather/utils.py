"""工具函数模块。

这里放置项目中常用的小工具函数。
"""

import os
from datetime import datetime

import pygame


SCREENSHOTS_FOLDER = "screenshots"


def save_screenshot(screen):
    """保存当前画面截图，并返回保存路径。"""
    # 如果 screenshots 文件夹不存在，就自动创建
    os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)

    # 使用当前时间生成文件名，避免覆盖旧截图
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"weather_{timestamp}.png"
    file_path = os.path.join(SCREENSHOTS_FOLDER, filename)

    # 使用 Pygame 保存当前屏幕画面
    pygame.image.save(screen, file_path)
    return file_path