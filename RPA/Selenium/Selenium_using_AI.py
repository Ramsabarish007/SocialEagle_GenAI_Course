from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class HerokuAppTests:
    BASE_URL = "https://the-internet.herokuapp.com/"

    def __init__(self):
        options = webdriver.ChromeOptions()

        # Disable password manager prompts and notifications
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        # Additional switches to block password popups & automation detection
        options.add_argument("--incognito")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-password-manager-reauthentication")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def go_home(self):
        self.driver.get(self.BASE_URL)

    # 1️⃣ Form Authentication
    def test_login(self):
        self.go_home()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Form Authentication"))
        ).click()

        self.wait.until(EC.visibility_of_element_located(
            (By.ID, "username"))
        ).send_keys("tomsmith")

        self.wait.until(EC.visibility_of_element_located(
            (By.ID, "password"))
        ).send_keys("SuperSecretPassword!")

        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))
        ).click()

        success = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "flash"))
        ).text

        assert "You logged into a secure area!" in success
        print("Login test passed")

    # 2️⃣ Checkboxes
    def test_checkboxes(self):
        self.go_home()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Checkboxes"))
        ).click()

        checkboxes = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "input[type='checkbox']"))
        )

        if not checkboxes[0].is_selected():
            checkboxes[0].click()
        if checkboxes[1].is_selected():
            checkboxes[1].click()

        print("Checkbox test passed")

    # 3️⃣ Dropdown
    def test_dropdown(self):
        self.go_home()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Dropdown"))
        ).click()

        dropdown_element = self.wait.until(EC.presence_of_element_located(
            (By.ID, "dropdown"))
        )

        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text("Option 2")

        assert dropdown.first_selected_option.text == "Option 2"
        print("Dropdown test passed")

    # 4️⃣ JavaScript Alert
    def test_alert(self):
        self.go_home()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "JavaScript Alerts"))
        ).click()

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Click for JS Alert']"))
        ).click()

        self.wait.until(EC.alert_is_present())
        Alert(self.driver).accept()

        result = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "result"))
        ).text

        assert "You successfully clicked an alert" in result
        print("Alert test passed")

    # 5️⃣ Dynamic Loading
    def test_dynamic_loading(self):
        self.go_home()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Dynamic Loading"))
        ).click()

        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Example 1: Element on page that is hidden"))
        ).click()

        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#start button"))
        ).click()

        message = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "finish"))
        ).text

        assert "Hello World!" in message
        print("Dynamic loading test passed")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    tests = HerokuAppTests()

    tests.test_login()
    tests.test_checkboxes()
    tests.test_dropdown()
    tests.test_alert()
    tests.test_dynamic_loading()

    tests.close()
