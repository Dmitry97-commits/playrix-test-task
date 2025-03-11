import subprocess

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService


def pytest_addoption(parser):
    parser.addoption("--platform_version", action="store", default=None, help="platform version")
    parser.addoption("--platform_name", action="store", default="Android", help="platform name")
    parser.addoption("--udid", action="store", default=None, help="udid of the device")
    parser.addoption("--unlock_type", action="store", default=None, help="unlock type")
    parser.addoption("--unlock_key", action="store", default=None, help="unlock key")

@pytest.fixture(scope="session")
def set_platform(request):
    return request.config.getoption("--platform_name")

@pytest.fixture(scope="session")
def set_version(request):
    return request.config.getoption("--platform_version")

@pytest.fixture(scope="session")
def set_udid(request):
    return request.config.getoption("--udid")

@pytest.fixture(scope="session")
def set_unlock_type(request):
    return request.config.getoption("--unlock_type")

@pytest.fixture(scope="session")
def set_unlock_key(request):
    return request.config.getoption("--unlock_key")

@pytest.fixture(scope="session", autouse=True)
def start_appium_server():
    service = AppiumService()
    service.start()
    yield
    service.stop()

def get_android_udid():
    output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip()
    lines = output.splitlines()

    for line in lines[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                return parts[0]
    return None

def get_android_platform_version():
    output = subprocess.check_output(
        ["adb", "shell", "getprop", "ro.build.version.release"]
    )
    version = output.decode("utf-8").strip()
    if version:
        return version
    return None


@pytest.fixture(scope="session")
def driver(set_platform, set_version, set_udid, set_unlock_type, set_unlock_key):
    options = UiAutomator2Options()
    options.platform_name = set_platform
    options.platform_version = set_version if not set_version else get_android_platform_version()
    options.device_name = "MyOwnAndroidDevice"
    options.udid = set_udid if set_udid else get_android_udid()
    options.app_package = "com.playrix.township"
    options.app_wait_activity = "com.playrix.township.*"
    options.unlock_type = set_unlock_type
    options.unlock_key = set_unlock_key
    options.auto_grant_permissions = True
    options.no_reset = False

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options
    )
    yield driver
    driver.quit()

