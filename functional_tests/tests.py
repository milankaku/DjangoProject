from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # user goes to home page
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user sees input area and enters a todo list item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy some milk')

        # When user hits enter, the page updates, and now the page lists new item
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some milk')

        # text box to enter a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to sleep early')
        inputbox.send_keys(Keys.ENTER)

        # The page updates, and now shows both items on the user's list
        self.wait_for_row_in_list_table('2: Go to sleep early')
        self.wait_for_row_in_list_table('1: Buy some milk')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user goes to home page and enters own to do list item
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to sleep early')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Go to sleep early')

        # user's todo list has a unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # Now a new user comes to homepage.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # New User visits the home page.  There is no items from other user's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Go to sleep early', page_text)
        self.assertNotIn('some milk', page_text)

        # New user enters new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to practice')
        inputbox.send_keys(Keys.ENTER)
        #self.check_for_row_in_list_table('1: Go to practice')

        # New user gets unique URL
        new_user_list_url = self.browser.current_url
        self.assertRegex(new_user_list_url, '/lists/.+')
        self.assertNotEqual(new_user_list_url, first_user_list_url)

        # no items from original user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Go to sleep early', page_text)
        self.assertNotIn('some milk', page_text)
