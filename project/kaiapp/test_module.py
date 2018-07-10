# import unittest
#
#
# def setUpModule():
#     print('In setUpModule()...')
#
#
# def tearDownModule():
#     print('In tearDownModule()...')
#
#
# class TestClass(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         print('In setUpClass()...')
#
#     @classmethod
#     def tearDownModule(cls):
#         print('In tearDownModule()...')
#
#     def setUp(self):
#         print('\nIn setUp()...')
#
#     def tearDown(self):
#         print('\nIn tearDownModule()...')
#
#     def test_class01(self):
#         stack = Stack(10)
#         self.assertTrue(stack.len() ==  0)
#         stack.add(1)
#         stack.add(2)
#         self.assertTrue(stack.len() == 1)
#         item = stack.pop()
#         self.assertTrue(item == 1)
#         self.assertTrue('PYTHON'.isupper())
#         print('In test_class01()...')
#
#
# # 堆栈
# class Stack(object):
#     def __init__(self, stack_size):
#         self.stack = []
#         self.stack_size = stack_size
#
#     def add(self, item):
#         self.stack.append(item)
#         return self.stack
#
#     def pop(self):
#         return self.stack[-1]
#
#     def len(self):
#         return len(self.stack)
#
#     def is_empty(self):
#         if len(self.stack):
#             return False
#         else:
#             return True
#
#     def is_full(self):
#         if len(self.stack) == self.stack_size:
#             return True
#         else:
#             return False
#
#     def remove_all(self):
#         while True:
#             if self.stack > 0:
#                 return self.stack.pop(-1)
#             break
#
#     def index(self):
#         return
#
#
# if __name__ == '__main__':
#     unittest.main()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.timeout = 40
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    # def tearDown(self):
    #     self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('https://www.baidu.com')

        self.assertIn('百度', self.browser.title)
        login_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, '登录')))
        login_link.click()

        login_link_2 = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__footerULoginBtn')))

        login_link_2.click()

        username_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__userName')))
            # EC.presence_of_element_located((By.XPATH, '//*[@id="TANGRAM__PSP_10__userName"]')))
        username_input.clear()
        username_input.send_keys('流星陨落KKK')

        password_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_10__password')))
        password_input.clear()
        password_input.send_keys('qu19931202kai')

        # ver_code_input = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="TANGRAM__PSP_3__verifyCodeImg"]')))
        # ver_code_input.clear()
        # ver_code_input.send_keys('*****')

        login_submit_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__submit')))
        login_submit_button.click()

        username_span = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#s_username_top > span')))
        self.assertEqual(username_span.text, 'PebbleApp')

    # user_login_link = self.browser.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn')
    # user_login_link.click()


if __name__ == '__main__':
    unittest.main(warnings='ignore')