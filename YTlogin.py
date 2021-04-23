import os
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#geckodriver_autoinstaller.install()

profile = webdriver.FirefoxProfile('C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/xxxxxxxx.default')

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired)
