import mechanize
import cookielib
from copy import deepcopy
from kivy.clock import Clock
from threading import Thread
from functools import partial
from time import sleep
import BaseBrowser
import common
import bs4

class _SISMessage:
    #https://my.ibu.edu.ba/pages/p401.php?id=msgId
    msgFrom = None
    msgTitle = None
    msgDate = None
    msgContent = None
    msgId = None
    def getUrl(self):
        return 'https://my.ibu.edu.ba/pages/p401.php?id='+msgId
        
class _SISCourse:
    courseName = None
    courseCode = None
    courseGrades = None
    courseExamDates = None
    courseLecturer = None
    courseLMSAlias = None

class _SISData:
    pictureUrl = None
    nameSurname = None
    department = None
    eMail = None
    messages = None
    courses = None
    studentID = None

class SISBrowser(BaseBrowser.BaseBrowser):
    runFunction = None
    def __init__(self, resultFunction = None, errorFunction = None, updateFunction = None, maxUpdatesFunction = None):
        BaseBrowser.BaseBrowser.__init__(self, resultFunction, errorFunction, updateFunction, maxUpdatesFunction)
        global cookiejar
        if cookiejar is not None:
            #self.cookies = cookiejar
            self.browser.set_cookiejar(cookiejar)

    def login(self, username, password):
        self.runFunction = partial(self._login, username, password)
        
    def getUserInfo(self):
        self.runFunction = self._getUserInfo

    def _login(self, username, password):
        global cookiejar
        if (not cookiejar == None):
            raise Exception("User already logged in. Try logging out first")
        self.getPage("https://my.ibu.edu.ba/index.php")
        self.callUpdateFunction()
        self.browser.select_form(name = "cover")
        self.browser.form['username'] = username
        self.browser.form['password'] = password
        self.browser.submit()
        if (self.getPage("https://my.ibu.edu.ba/pages/home.php").find('LOGOUT')>=0):
            cookiejar = deepcopy(self.cookies)
            Clock.schedule_once(self.resultFunction,0)
            return
        raise Exception("Invalid username/password")
        
    def _getUserInfo(self):
        global SISData
        if SISData is None:
            SISData = _SISData()
        bs = bs4.BeautifulSoup(self.getPage("https://my.ibu.edu.ba/pages/home.php"))
        found = bs.find_all('td', height='20')
        SISData.studentID = str(found[1].get_text()).strip()
        SISData.namesurname = str(found[3].get_text()).strip()
        SISData.department = str(found[5].get_text()).strip()
        SISData.eMail = str(found[7].get_text()).strip()
        SISData.messages = []
        for t in bs.find_all('td', class_='box', valign='top'):
            if (t.find('b')):
                if (t.find('b').find('a')):
                    #print '  -->  href -',t.find('b').find('a')['href']
                    SISData.messages.append(_SISMessage())
                    s = str(t.find('b').find('a')['href'])
                    SISData.messages[-1].msgId=s[s.find('?id=')+4:]
                    #print SISData.messages[-1].msgId
        Clock.schedule_once(self.resultFunction,0)

cookiejar = None
SISData = None

def reset():
    global cookiejar
    global SISData
    cookiejar = None
    SISData = None
    BaseBrowser.cachedPages = {}