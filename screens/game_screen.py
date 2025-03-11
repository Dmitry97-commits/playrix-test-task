import random

from appium.webdriver.common.appiumby import AppiumBy
from helpers.logger import get_logger
from selenium.webdriver.support import expected_conditions as EC

from screens.base_screen import BaseScreen

logger = get_logger(__name__)

class GameScreen(BaseScreen):
    SCREEN_LOCATOR = (AppiumBy.ID, "android:id/content")
    COORDINATES_OF_ERNIE = (264, 901)
    COORDINATES_OF_WHEAT_ELEMENTS = {
        "wheat_bar": (1145, 960),
        "wheat_field_1": (1172, 500),
        "wheat_field_2": (1004, 559),
        "wheat_field_3": (1165, 641),
        "wheat_field_4": (1316, 569),
        "wheat_field_5": (1474, 494),
        "wheat_field_6": (1313, 432),
    }

    def wait_for_screen_is_present(self):
        logger.info("Wait for screen to be visible")
        self.wait_until(EC.visibility_of_element_located(self.SCREEN_LOCATOR))

    def click_on_screen(self):
        logger.info("Click on screen")
        self.click(self.SCREEN_LOCATOR)

    def click_on_ernie(self):
        logger.info("Click by coordinates on Ernie")
        self.tap_by_coordinates(*self.COORDINATES_OF_ERNIE)

    def sow_the_random_field(self):
        self.tap_by_coordinates(1199, 599)
        random_coordinates = self.COORDINATES_OF_WHEAT_ELEMENTS[f"wheat_field_{random.randint(1, 6)}"]
        logger.info(f"Sow the random field by coordinates {random_coordinates}")
        self.tap_by_coordinates(*random_coordinates)
        self.drag_and_drop_by_coordinates(*self.COORDINATES_OF_WHEAT_ELEMENTS["wheat_bar"], *random_coordinates)