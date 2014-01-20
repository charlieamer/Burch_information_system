from threading import Thread
from time import sleep
from kivy.clock import Clock
from functools import partial
import mechanize
import sys
cachedPages = {}

class BaseBrowser(Thread):
    runFunction = None
    cachedPages = {}
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
            print 'BaseBrowser.run -> Browser error:',str(sys.exc_info()[1])
            if self.errorFunction is not None:
                Clock.schedule_once(partial(self.errorFunction, str(sys.exc_info()[1])),1)
    
    def getPage(self, url, force=False):
        try:
            assert(not force)
            ret = cachedPages[url]
            print 'BaseBrowser.getPage -> returning cached version of:',url
            return ret
        except:
            self.browser.open(url)
            cachedPages[url]=self.browser.response().read()
            print 'BaseBrowser.getPage -> returning internet version of:',url
            return cachedPages[url]
            

    def callUpdateFunction(self):
        if self.updateFunction is not None:
            Clock.schedule_once(self.updateFunction,0)

    def callMaxUpdatesFunction(self, maxupdates):
        if self.maxUpdatesFunction is not None:
            Clock.schedule_once(partial(self.maxUpdatesFunction, maxupdates))