from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewUserTest(unittest.TestCase):

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
        self.browser.get('http://127.0.0.1:8000/')

        self.assertIn('To Do List', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To Do', header)


        inputarea = self.browser.find_element_by_id('id_new_task')
        self.assertEqual(inputarea.get_attribute('placeholder'), 'Enter a to do task')

        inputarea.send_keys('Buy some milk tomorrow')
        inputarea.send_keys(Keys.ENTER)

        self.check_for_row_in_table('1: Buy some milk tomorrow')

        inputarea = self.browser.find_element_by_id('id_new_task')
        inputarea.send_keys('Buy some potatoes today')
        inputarea.send_keys(Keys.ENTER)

        self.check_for_row_in_table('1: Buy some milk tomorrow')
        self.check_for_row_in_table('2: Buy some potatoes today')

        self.fail('Add testing for input box to add more to do tasks')

if __name__ == '__main__':
    unittest.main()