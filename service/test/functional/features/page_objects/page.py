#
# Copyright (c) 2015 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Page:
    def __init__(self, driver):
        self.webdriver = driver

    def wait_until_element_is_deleted(self, locator_tuple, timeout=10):
        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(lambda s: len(s.find_elements(locator_tuple[0], locator_tuple[1])) == 0)

    def wait_for_user_alert_to_disappear(self,  timeout=10):
        self.wait_until_element_is_invisible_by_locator((By.ID, 'user-alerts'), timeout)

    def wait_until_element_is_invisible_by_locator(self,  locator_tuple, timeout=10):
        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(EC.invisibility_of_element_located(locator_tuple))

    def wait_until_elements_are_visible_by_locator(self, locator_tuple, timeout=10):
        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(EC.presence_of_all_elements_located(locator_tuple))
        return self.webdriver.find_elements(locator_tuple[0], locator_tuple[1])

    def wait_until_element_is_visible_by_locator(self, locator_tuple, timeout=10):
        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(EC.visibility_of_element_located(locator_tuple))
        return self.webdriver.find_element(locator_tuple[0], locator_tuple[1])

    def fill_by_xpath(self, xpath, text):
        field = self.webdriver.find_element_by_xpath(xpath)
        field.send_keys(text)

    def take_screenshot(self, filename):
        self.webdriver.save_screenshot(filename)

    def dump_source_to(self, filename):
        with open(filename, 'w') as out:
            out.write(self.webdriver.page_source.encode('utf8'))

    def page_has_css(self, css):
        try:
            self.find_element_by_css_selector(css)
            return True
        except TimeoutException:
            return False

    def find_element_by_xpath(self, xpath):
        return self.wait_until_element_is_visible_by_locator(By.XPATH, xpath)

    def find_element_by_id(self, id):
        return self.wait_until_element_is_visible_by_locator(By.ID, id)

    def find_element_by_css_selector(self, css_selector):
        return self.wait_until_element_is_visible_by_locator(By.CSS_SELECTOR, css_selector)

    def find_elements_by_css_selector(self, css_selector):
        return self.wait_until_elements_are_visible_by_locator(By.CSS_SELECTOR, css_selector)

    def find_element_containing_text(self, text, element_type='*'):
        return self.find_element_by_xpath("//%s[contains(.,'%s')]" % (element_type, text))

    def element_should_have_content(self, css_selector, content):
        e = self.find_element_by_css_selector(css_selector)
        assert e.text == content

    def wait_until_button_is_visible(self, title, timeout=10):
        wait = WebDriverWait(self.webdriver, timeout)
        locator_tuple = (By.XPATH, ("//%s[contains(.,'%s')]" % ('button', title)))
        wait.until(EC.visibility_of_element_located(locator_tuple))

    def click_button(self, title, element='button'):
        button = self.find_element_containing_text( title, element_type=element)
        button.click()

    def mail_subject(self):
        e = self.find_element_by_css_selector( '#mail-view .subject')
        return e.text

    def reply_subject(self):
        e = self.find_element_by_css_selector('#reply-subject')
        return e.text

    def get_console_log(self):
        logs = self.webdriver.get_log('browser')
        for entry in logs:
            msg = entry['message']
            if not (msg.startswith('x  off') or msg.startswith('<- on')):
                print entry['message']