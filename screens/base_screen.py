from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait

from helpers.logger import get_logger

logger = get_logger(__name__)

class BaseScreen:
    def __init__(self, driver, default_timeout=15):
        self.driver = driver
        self.timeout = default_timeout

    def find_element(self, by: str, value: str):
        logger.info(f"Find element by locator {by, value}")
        return self.driver.find_element(by, value)

    def click(self, locator):
        logger.info(f"Click on locator {locator}")
        return self.find_element(*locator).click()

    def wait_until(self, condition: EC, timeout=None):
        logger.info(f"Wait until condition {condition}")
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(condition)

    def wait_implicitly(self, time_to_wait):
        logger.info(f"Wait implicitly {time_to_wait} sec")
        return self.driver.implicitly_wait(time_to_wait)

    def tap_by_coordinates(self, x, y):
        logger.info(f"Tap by coordinates {x, y}")
        pointer_input = PointerInput(POINTER_TOUCH, "finger1")
        actions = ActionBuilder(self.driver, mouse=pointer_input)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pointer_up()
        actions.pointer_action.pause(2)
        actions.perform()

    def drag_and_drop_by_coordinates(self, start_x, start_y, end_x, end_y):
        logger.info(f"Drag by coordinates {start_x, start_y}, {end_x, end_y}")
        pointer_input = PointerInput(POINTER_TOUCH, "finger1")
        actions = ActionBuilder(self.driver, mouse=pointer_input)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.pointer_up()
        actions.perform()