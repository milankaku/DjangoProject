from selenium import webdriver
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
        self.fail(self.browser.title)

if __name__ == '__main__':
    unittest.main()