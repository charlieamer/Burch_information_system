import mechanize
import cookielib
from copy import deepcopy
from kivy.clock import Clock
from threading import Thread
from functools import partial
from time import sleep
from common import BaseBrowser

cookiejar = None

class LMSBrowser(BaseBrowser):
    runFunction = None
    def __init__(self, resultFunction, errorFunction, updateFunction = None, maxUpdatesFunction = None):
        BaseBrowser.__init__(self, resultFunction, errorFunction, updateFunction, maxUpdatesFunction)
        global cookiejar
        if cookiejar is not None:
            self.cookies = cookiejar

    def login(self, username, password):
        self.runFunction = partial(self._login, username, password)

    def _login(self, username, password):
        global cookiejar
        if (not cookiejar == None):
            raise Exception("User already logged in. Try logging out first")
        self.browser.open("http://lms.ibu.edu.ba/login/index.php")
        self.callUpdateFunction()
        self.browser.select_form(nr=0)
        self.browser.form['username'] = username
        self.browser.form['password'] = password
        self.browser.submit()
        if (self.browser.response().read().find('You are logged in as')>=0):
            cookiejar = deepcopy(self.cookies)
            Clock.schedule_once(self.resultFunction,0)
            return
        raise Exception("Invalid username/password")
