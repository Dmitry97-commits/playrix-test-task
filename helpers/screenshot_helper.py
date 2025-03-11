import os
import time

import cv2
import numpy as np

from helpers.logger import get_logger

logger = get_logger()

def get_path_to_screenshot(name_screenshot):
    logger.info(f"Get path to screenshot: {name_screenshot}")
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots", name_screenshot))
    return path

def find_image_on_screen(driver, screenshot, threshold=0.8):
    logger.info(f"Find image on screenshot: {screenshot}")
    path = get_path_to_screenshot(screenshot)
    screenshot_bytes = driver.get_screenshot_as_png()
    screenshot_array = np.frombuffer(screenshot_bytes, np.uint8)
    screenshot_img = cv2.imdecode(screenshot_array, cv2.IMREAD_COLOR)
    template_img = cv2.imread(path, cv2.IMREAD_COLOR)

    res = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return max_loc
    else:
        return None

def wait_for_image(driver, screenshot, timeout=10, threshold=0.8):
    logger.info(f"Wait for image: {screenshot}")
    start_time = time.time()
    while time.time() - start_time < timeout:
        coords = find_image_on_screen(driver, screenshot, threshold=threshold)
        if coords is not None:
            return coords
        time.sleep(0.1)
    return None

def compare_current_screen_by_feature(driver, screenshot: str,
                                      distance_threshold: float = 60.0, min_good_matches: int = 25):
    logger.info(f"Compare current screen: {screenshot}")
    screenshot_bytes = driver.get_screenshot_as_png()
    screenshot_array = np.frombuffer(screenshot_bytes, np.uint8)
    current_img = cv2.imdecode(screenshot_array, cv2.IMREAD_COLOR)

    path = get_path_to_screenshot(screenshot)
    reference_img = cv2.imread(path, cv2.IMREAD_COLOR)

    if len(current_img.shape) == 3:
        current_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)
    else:
        current_gray = current_img

    if len(reference_img.shape) == 3:
        reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
    else:
        reference_gray = reference_img

    orb = cv2.ORB_create()
    kp_cur, des_cur = orb.detectAndCompute(current_gray, None)
    kp_ref, des_ref = orb.detectAndCompute(reference_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_cur, des_ref)

    good_matches = [m for m in matches if m.distance < distance_threshold]
    is_similar = len(good_matches) >= min_good_matches

    return is_similar