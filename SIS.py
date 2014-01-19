import mechanize
import cookielib
from copy import deepcopy
from kivy.clock import Clock
from threading import Thread
from functools import partial
from time import sleep
from common import BaseBrowser

cookiejar = None

class SISBrowser(BaseBrowser):
    runFunction = None
    def __init__(self, resultFunction, errorFunction, updateFunction = None):
        BaseBrowser.__init__(self, resultFunction, errorFunction, updateFunction)
        global cookiejar
        if cookiejar is not None:
            self.cookies = cookiejar

    def login(self, username, password):
        self.runFunction = partial(self._login, username, password)

    def _login(self, username, password):
        global cookiejar
        if (not cookiejar == None):
            raise Exception("User already logged in. Try logging out first")
        self.browser.open("https://my.ibu.edu.ba/index.php")
        self.callUpdateFunction()
        self.browser.select_form(name = "cover")
        self.browser.form['username'] = username
        self.browser.form['password'] = password
        self.browser.submit()
        self.browser.open("https://my.ibu.edu.ba/pages/home.php")
        if (self.browser.response().read().find('LOGOUT')>=0):
            cookiejar = deepcopy(self.cookies)
            Clock.schedule_once(self.resultFunction,0)
            return
        raise Exception("Invalid username/password")
