import kivy
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from time import sleep
import pickle
import sys
import LMS
import SIS
import common
import os
import urllib

class LoginScreen(Screen):

    def resetCookieJar(self):
        self.hadError = True

    def tryLogin(self):
        if self.ids.login.text == "Logging in":
            return
        self.startLoggingIn()
        self.startLMSLogin()

    def updateFunction(self, dt=None):
        self.ids.login.value += 1.0

    def startLoggingIn(self):
        self.ids.login.text = "Logging in"
        self.ids.login.working = True
        self.ids.login.max = 4
        self.ids.login.value = 0
        self.ids.SIS_error.text = ""
        self.ids.LMS_error.text = ""
        self.hadError = False

    def finishLoggingIn(self):
        self.ids.login.working = False
        self.ids.login.text = "Login"
        self.ids.login.value = 4
        if (self.hadError):
            LMS.cookiejar = None
            SIS.cookiejar = None

    def startSISLogin(self):
        self.ids.login.value = 2
        li = common.LoginInfo(self.ids.SIS_username.text, self.ids.SIS_password.text, self.ids.SIS_use.active)
        LoginProvider.isSISLoginInfoValid(li, self.gotSISResult, self.gotSISError, self.updateFunction)

    def startLMSLogin(self):
        li = common.LoginInfo(self.ids.LMS_username.text, self.ids.LMS_password.text, self.ids.LMS_use.active)
        LoginProvider.isLMSLoginInfoValid(li, self.gotLMSResult, self.gotLMSError, self.updateFunction)

    def gotSISResult(self, dt):
        print "SIS login valid"
        self.finishLoggingIn()

    def gotSISError(self, e, dt):
        self.ids.SIS_error.text = e.message
        self.resetCookieJar()
        self.finishLoggingIn()
        
    def gotLMSResult(self, dt):
        print "LMS login valid"
        self.startSISLogin()

    def gotLMSError(self, e, dt):
        self.ids.LMS_error.text = e.message
        self.resetCookieJar()
        self.startSISLogin()
    
    
class LoginInformation:
    LMS = None
    SIS = None
    
class _LoginProvider:

    # Class for managing login information
    class LoginSingleton:
            
        def __init__(self):
            print 'Login provider constructed'
            if self.getLoginInformation() == None:
                print 'No valid login information found'
            else:
                print 'Login information loaded successfuly'
                
        def getLoginInformation(self):
            ret = None
            try:
                ret = pickle.load(open("data/loginInfo","rb"))
            except IOError as e:
                print "<IOError> Error opening login file:", e.strerror
            except:
                print "Unexpected error:", sys.exc_info()[0]
            return ret
            
        def writeLoginInformation(self, LoginInfo):
            try:
                pickle.dump(LoginInfo, open("data/loginInfo","wb"))
            except IOError as e:
                print "Error writing login file:", e.strerror
                
        def setLoginInformation(self, SISUsername, SISPassword, SISUse, LMSUsername, LMSPassword, LMSUse):
            info = LoginInformation()
            info.LMS = common.LoginInfo(LMSUsername, LMSPassword, LMSUse)
            info.SIS = common.LoginInfo(SISUsername, SISPassword, SISUse)
            self.writeLoginInformation(info)
        
        def deleteLoginInformation(self):
            try:
                os.remove("data/loginInfo")
            except:
                print "Couldn't delete login information, probably already deleted"
        
        def isValid(self, a, b):
            self.resultFunction(True)
        
        def isSISLoginInfoValid(self, LoginInfo, resultFunction, errorFunction = None, updateFunction = None):
            SIS.SISBrowser(resultFunction,errorFunction,updateFunction).login(LoginInfo.username, LoginInfo.password)
            
        def isLMSLoginInfoValid(self, LoginInfo, resultFunction, errorFunction = None, updateFunction = None):
            LMS.LMSBrowser(resultFunction,errorFunction,updateFunction).login(LoginInfo.username, LoginInfo.password)
            
    instance = None
    def __init__(self):
        if (_LoginProvider.instance == None):
            _LoginProvider.instance = _LoginProvider.LoginSingleton()
        else:
            print 'LoginProvider already exists'

LoginProvider = _LoginProvider().instance