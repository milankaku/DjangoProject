from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewUserTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_todo_list_and_retrieve_later(self):
        self.browser.get('http://127.0.0.1:8000/')

        self.assertIn('To Do List', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To Do', header)


        inputarea = self.browser.find_element_by_id('id_new_task')
        self.assertEqual(inputarea.get_attribute('placeholder'), 'Enter a to do task')

        inputarea.send_keys('Buy some milk tomorrow')
        inputarea.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == 'Buy some milk tomorrow' for row in rows), "To do task not in table")

        self.fail('Add testing for input box to add more to do tasks')

if __name__ == '__main__':
    unittest.main()