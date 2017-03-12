from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewUserTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_create_todo_list_and_retrieve_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To Do List', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To Do', header)

        inputarea = self.browser.find_element_by_id('id_new_task')
        self.assertEqual(inputarea.get_attribute('placeholder'), 'Enter a to do task')

        # When enter, taken to unique URL with the to do list and new item showing
        inputarea.send_keys('Buy some milk tomorrow')
        inputarea.send_keys(Keys.ENTER)
        milan_list_url = self.browser.current_url
        self.assertRegex(milan_list_url, 'lists/.+')
        self.check_for_row_in_table('1: Buy some milk tomorrow')

        inputarea = self.browser.find_element_by_id('id_new_task')
        inputarea.send_keys('Buy some potatoes today')
        inputarea.send_keys(Keys.ENTER)

        self.check_for_row_in_table('1: Buy some milk tomorrow')
        self.check_for_row_in_table('2: Buy some potatoes today')

        # New user comes to make a to do list , new browser
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # New user sees home page. not other users lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy some milk tomorrow', page_text)
        self.assertNotIn('potatoes today', page_text)

        # New user starts new list and gets unique URL
        inputarea = self.browser.find_element_by_id('id_new_task')
        inputarea.send_keys('Go to sleep early')
        inputarea.send_keys(Keys.ENTER)

        new_user_list_url = self.browser.current_url
        self.assertRegex(new_user_list_url, 'lists/.+')
        self.assertNotEqual(new_user_list_url, milan_list_url)

        # Make sure after new user goes to their to do list, they are not seeing first user's to do items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy some milk tomorrow', page_text)
        self.assertNotIn('potatoes today', page_text)

        self.fail('Add testing for input box to add more to do tasks')
