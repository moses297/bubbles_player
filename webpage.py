from selenium import webdriver
import pyautogui


script = '''
    var s = document.createElement('script');
    s.src = 'fix_swf.js';
    document.body.appendChild(s);
'''

def open_url(url):
    browser = webdriver.Firefox()
    browser.get(url)
    browser.set_window_size(950, 800)
    browser.execute_script(script)

    browser.save_screenshot('test1.png')
    e = browser.find_element_by_css_selector("object[width='600px'][height='480px']")
    return e.location


