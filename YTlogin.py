import os
from time import sleep, time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def connect_to_base(driver, base_url):
        
    print("Jenkins Pull Request url:- "+base_url)

    try:
            driver.get(base_url.strip())
            # wait for table element with id = 'hnmain' to load
            # before returning True
            wait = WebDriverWait(driver, 5)
            wait.until(visibility_of_element_located((By.XPATH, "//*[@class='yt-simple-endpoint style-scope ytd-button-renderer']")))
            return True
            
    except:
            print(f"WARNING: required elements not loaded to get open requests from {base_url}.")
            return True

geckodriver_autoinstaller.install()

profilepath='/Users/imsathiya17/Library/Application Support/Firefox/Profiles/1owiyum0.default'

print(profilepath)

#useragent = "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"
#useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"

profile = webdriver.FirefoxProfile(profilepath)

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()

desired = DesiredCapabilities.FIREFOX

options = webdriver.FirefoxOptions()
#profile.set_preference("general.useragent.override", useragent)
options.set_preference("dom.webnotifications.serviceworker.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)
#options.add_argument('--headless')
options.add_argument('disable-blink-features=AutomationControlled')
#options.set_preference("excludeSwitches", ["enable-automation"])
options.set_preference("useAutomationExtension", False)
#options.add_option("excludeSwitches", ["enable-automation"])
#options.add_option('useAutomationExtension', False)

driver = webdriver.Firefox(firefox_profile=profile,options=options,desired_capabilities=desired)
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

base_url="https://www.youtube.com/c/CryptoTamil/about"

driver.get(base_url.strip())
sleep(5)

driver.maximize_window()

driver.execute_script("window.scrollTo(0, 790)")

sleep(2)

print(driver.get_window_size())


selfApproveButton=driver.find_element_by_xpath('//ytd-button-renderer[@class="style-scope ytd-channel-about-metadata-renderer style-default size-default"]')

print("Element is visible? " + str(selfApproveButton.is_displayed()))

selfApproveButton.click()

sleep(5)

iframe = driver.find_elements_by_tag_name('iframe')[0]

driver.switch_to.frame(iframe)

driver.implicitly_wait(30)

captchacb=driver.find_element_by_xpath('//span[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox"]')

print("captchacb is visible? " + str(captchacb.is_displayed()))

captchacb.click()