from threading import Thread
from time import sleep
from kivy.clock import Clock
from functools import partial
import mechanize
from requests.exceptions import HTTPError
import sys
from kivy.uix.screenmanager import ScreenManager

MainScreenManager = ScreenManager()

class LoginInfo:
    username = None
    password = None
    use = False
    def __init__(self, username, password, use):
        self.username = username
        self.password = password
        self.use = use
    def asList(self):
        return {'username':self.username, 'password':self.password}

class BaseBrowser(Thread):
    runFunction = None
    def __init__(self, resultFunction, errorFunction, updateFunction, maxUpdatesFunction):
        Thread.__init__(self)
        self.errorFunction = errorFunction
        self.updateFunction = updateFunction
        self.resultFunction = resultFunction
        self.maxUpdatesFunction = maxUpdatesFunction
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.cookies = self.browser._ua_handlers['_cookies'].cookiejar
        self.start()

    def run(self):
        while not self.runFunction:
            sleep(.1)
        try:
            self.runFunction()
        except:
            print 'Browser error:',str(sys.exc_info()[1])
            if self.errorFunction is not None:
                Clock.schedule_once(partial(self.errorFunction, str(sys.exc_info()[1])),1)

    def callUpdateFunction(self):
        if self.updateFunction is not None:
            Clock.schedule_once(self.updateFunction,0)

    def callMaxUpdatesFunction(self, maxupdates):
        if self.maxUpdatesFunction is not None:
            Clock.schedule_once(partial(self.maxUpdatesFunction, maxupdates))