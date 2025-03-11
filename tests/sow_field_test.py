from helpers.screenshot_helper import wait_for_image, compare_current_screen_by_feature
from screens.game_screen import GameScreen
from screens.start_screen import StartScreen


def test_sow_the_random_field(driver):
    start_screen = StartScreen(driver)
    start_screen.close_user_agreement_popup_with_ok()

    game_screen = GameScreen(driver)
    game_screen.wait_for_screen_is_present()
    assert wait_for_image(driver, "ernie.png"), "Ernie is not present on the screen"

    game_screen.click_on_ernie()
    game_screen.click_on_screen()
    game_screen.sow_the_random_field()
    assert compare_current_screen_by_feature(driver, "sown_field.png"), "The field is not sown"
