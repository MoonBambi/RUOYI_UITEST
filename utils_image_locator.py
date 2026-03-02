import os
import time
import logging
from typing import Optional, Tuple

import pyautogui

try:
    import pyperclip  # type: ignore
except ImportError:
    pyperclip = None


class ImageLocator:
    @staticmethod
    def get_image_path(image_name: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(base_dir, "pages", "imgs")
        image_path = os.path.join(image_dir, image_name)
        if os.path.exists(image_path):
            return image_path
        logging.error(f"图像文件不存在: {image_path}")
        raise FileNotFoundError(f"图像文件不存在: {image_path}")

    @staticmethod
    def locate_on_screen(
        image_name: str,
        confidence: float = 0.8,
        max_attempts: int = 3,
        wait_time: float = 1.0,
        grayscale: bool = True,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[Tuple[int, int]]:
        image_path = ImageLocator.get_image_path(image_name)
        for attempt in range(max_attempts):
            try:
                location = pyautogui.locateOnScreen(
                    image_path,
                    confidence=confidence,
                    grayscale=grayscale,
                    region=region,
                )
                if location:
                    point = pyautogui.center(location)
                    logging.info(
                        f"识别到图像 {image_name} 于 ({point.x}, {point.y})，尝试次数 {attempt + 1}"
                    )
                    return point.x, point.y
            except Exception as e:
                logging.error(f"图像识别尝试 {attempt + 1} 失败: {e}")
            time.sleep(wait_time)
        return None

    @staticmethod
    def image_exists(image_name: str, **kwargs) -> bool:
        center = ImageLocator.locate_on_screen(image_name, **kwargs)
        if center:
            logging.info(f"识别到图像 {image_name}")
            return True
        return False

    @staticmethod
    def image_click(image_name: str, **kwargs) -> bool:
        center = ImageLocator.locate_on_screen(image_name, **kwargs)
        if center:
            try:
                x, y = center
                logging.info(f"点击图像 {image_name} 于 ({x}, {y})")
                pyautogui.click(x, y)
                return True
            except Exception as e:
                logging.error(f"点击图像时发生错误: {e}")
                return False
        return False

    @staticmethod
    def image_click_and_write(
        image_name: str, text_to_write: str, **kwargs
    ) -> bool:
        center = ImageLocator.locate_on_screen(image_name, **kwargs)
        if center:
            try:
                x, y = center
                pyautogui.click(x, y)
                if pyperclip is not None:
                    pyperclip.copy(text_to_write)
                    pyautogui.hotkey("ctrl", "v")
                else:
                    pyautogui.typewrite(text_to_write)
                return True
            except Exception as e:
                logging.error(f"点击图像并输入时发生错误: {e}")
                return False
        return False
