from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from helpers.logger import get_logger
from screens.base_screen import BaseScreen

logger = get_logger(__name__)

class StartScreen(BaseScreen):
    AGREEMENT_LOCATOR = (AppiumBy.XPATH, "//android.widget.Button[@resource-id='com.playrix.township:id"
                                   "/system_dialog_button' and @text='ОК']")

    def close_user_agreement_popup_with_ok(self):
        logger.info("Close user agreement popup with ok")
        self.wait_until(EC.visibility_of_element_located(self.AGREEMENT_LOCATOR))
        self.click(self.AGREEMENT_LOCATOR)