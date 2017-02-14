from os.path import abspath
from selenium import webdriver
import ctypes
from platform import system


class Webpage(object):
    _web_driver_browser = None
    _window_handle = None
    _URL = 'file:///' + abspath('Bubble%20Game.html')
    _profile = webdriver.FirefoxProfile()
    _profile.set_preference('browser.fullscreen.autohide', True)
    _profile.set_preference('browser.fullscreen.animate', False)

    @classmethod
    def open_url(cls):
        cls._web_driver_browser = webdriver.Firefox(cls._profile)
        cls._window_handle = cls._get_active_window()
        cls._web_driver_browser.get(cls._URL)
        cls._web_driver_browser.set_window_size(800, 800)
        cls._web_driver_browser.save_screenshot('test1.png')
        e = cls._web_driver_browser.find_element_by_css_selector("object[width='600px'][height='480px']")
        return e.location

    @classmethod
    def is_active(cls):
        """
            :return: True iff game window is active or not on Windows platform
        """
        active_window = cls._get_active_window()
        return not active_window or cls._window_handle == active_window

    @classmethod
    def close(cls):
        cls._web_driver_browser.quit()

    @classmethod
    def _get_active_window(cls):
        """
            :return: On Windows platform returns the system handle of the active window,
                        Otherwise returns None
        """
        if system() == 'Windows':
            return ctypes.windll.user32.GetForegroundWindow()

