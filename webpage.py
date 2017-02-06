from os.path import abspath
from selenium import webdriver
import ctypes
from platform import system


class Webpage(object):
    _window_handle = None
    _URL = 'file:///' + abspath('Bubble%20Game.html')

    @classmethod
    def open_url(cls):
        script = "\n    var s = document.createElement('script');\n    s.src = 'fix_swf.js';\n    " \
                 "document.body.appendChild(s);\n "
        browser = webdriver.Firefox()
        cls._window_handle = cls._get_active_window()
        browser.get(cls._URL)
        browser.set_window_size(950, 800)
        browser.execute_script(script)
        browser.save_screenshot('test1.png')
        e = browser.find_element_by_css_selector("object[width='600px'][height='480px']")
        return e.location

    @classmethod
    def is_active(cls):
        """
            :return: True iff game window is active or not on Windows platform
        """
        active_window = cls._get_active_window()
        return not active_window or cls._window_handle == active_window

    @classmethod
    def _get_active_window(cls):
        """
            :return: On Windows platform returns the system handle of the active window,
                        Otherwise returns None
        """
        if system() == 'Windows':
            return ctypes.windll.user32.GetForegroundWindow()
