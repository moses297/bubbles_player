from os.path import abspath
from selenium import webdriver
import ctypes
from platform import system


class Webpage(object):
    _web_driver_browser = None
    _window_handle = None
    _URL = 'file:///' + abspath('Bubble%20Game.html')


    @classmethod
    def open_url(cls):
        script = "\n    var s = document.createElement('script');\n    s.src = 'fix_swf.js';\n    " \
                 "document.body.appendChild(s);\n "
        cls._web_driver_browser = webdriver.Firefox()
        cls._window_handle = cls._get_active_window()
        cls._web_driver_browser.get(cls._URL)
        cls._web_driver_browser.set_window_size(950, 800)
        cls._web_driver_browser.execute_script(script)
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

