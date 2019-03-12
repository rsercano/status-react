import pytest
from selenium.common.exceptions import NoSuchElementException

from support.device_apps import start_web_browser
from tests import marks
from tests.base_test_case import SingleDeviceTestCase
from views.sign_in_view import SignInView
from tests.users import basic_user


class TestDeepLinks(SingleDeviceTestCase):

    @marks.testrail_id(5396)
    @marks.high
    def test_open_public_chat_using_deep_link(self):
        sign_in_view = SignInView(self.driver)
        sign_in_view.create_user()
        self.driver.close_app()
        start_web_browser(self.driver)
        chat_name = sign_in_view.get_public_chat_name()
        sign_in_view.send_as_keyevent('https://get.status.im/chat/public/%s' % chat_name)
        sign_in_view.confirm()
        sign_in_view.open_in_status_from_external_browser_button.click()
        sign_in_view.sign_in()
        chat_view = sign_in_view.get_chat_view()
        try:
            assert chat_view.user_name_text.text == '#' + chat_name
        except (AssertionError, NoSuchElementException):
            pytest.fail("Public chat '%s' is not opened" % chat_name)

    @marks.testrail_id(5441)
    @marks.medium
    def test_open_user_profile_using_deep_link(self):
        sign_in_view = SignInView(self.driver)
        sign_in_view.create_user()
        self.driver.close_app()
        start_web_browser(self.driver)
        sign_in_view.send_as_keyevent('https://get.status.im/user/%s' % basic_user['public_key'])
        sign_in_view.confirm()
        sign_in_view.open_in_status_from_external_browser_button.click()
        sign_in_view.sign_in()
        chat_view = sign_in_view.get_chat_view()
        for text in basic_user['username'], 'Add to contacts', 'Send transaction':
            if not chat_view.element_by_text(text).scroll_to_element():
                pytest.fail("User profile screen is not opened")


    @marks.testrail_id(5442)
    @marks.medium
    def test_open_dapp_using_deep_link(self):
        sign_in_view = SignInView(self.driver)
        sign_in_view.create_user()
        self.driver.close_app()
        start_web_browser(self.driver)
        dapp_name = 'simpledapp.eth'
        sign_in_view.send_as_keyevent('https://get.status.im/browse/%s' % dapp_name)
        sign_in_view.confirm()
        sign_in_view.open_in_status_from_external_browser_button.click()
        sign_in_view.sign_in()
        web_view = sign_in_view.get_chat_view()
        try:
            test_dapp_view = web_view.open_in_status_button.click()
            test_dapp_view.allow_button.is_element_present()
        except NoSuchElementException:
            pytest.fail("DApp '%s' is not opened!" % dapp_name)

    @marks.testrail_id(5780)
    @marks.medium
    def test_open_own_user_profile_using_deep_link(self):
        sign_in_view = SignInView(self.driver)
        sign_in_view.recover_access(passphrase=basic_user['passphrase'])
        self.driver.close_app()
        start_web_browser(self.driver)
        sign_in_view.send_as_keyevent('https://get.status.im/user/%s' % basic_user['public_key'])
        sign_in_view.confirm()
        sign_in_view.open_in_status_from_external_browser_button.click()
        sign_in_view.sign_in()
        chat_view = sign_in_view.get_chat_view()
        for text in basic_user['username'], 'Share my profile', 'Contacts':
            if not chat_view.element_by_text(text).scroll_to_element():
                pytest.fail("Own profile screen is not opened!")

    @marks.testrail_id(5781)
    @marks.medium
    def test_deep_link_with_invalid_user_public_key(self):
        sign_in_view = SignInView(self.driver)
        sign_in_view.create_user()
        self.driver.close_app()
        start_web_browser(self.driver)
        sign_in_view.send_as_keyevent('https://get.status.im/user/%s' % basic_user['public_key'][:-10])
        sign_in_view.confirm()
        sign_in_view.open_in_status_from_external_browser_button.click()
        sign_in_view.sign_in()
        chat_view = sign_in_view.get_home_view()
        start_new_chat_view = chat_view.plus_button.click()
        try:
            assert start_new_chat_view.start_new_chat_button.is_element_present()
        except (AssertionError, NoSuchElementException):
            pytest.fail("Can't navigate to start new chat after app opened from deep link with invalid public key")
