from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from time import sleep
from common import MainScreenManager
from login import LoginProvider, LoginInformation, LoginInfo
import LMS
import SIS

class LoginScreen(Screen):
    """
    Controls login screen
    """
    def __init__(self):
        LMS.reset()
        SIS.reset()
        Screen.__init__(self, name="login")
        li = LoginProvider.getLoginInformation()
        if li is not None:
            LoginProvider.deleteLoginInformation()
            self.ids.SIS_username.text = li.SIS.username
            self.ids.SIS_password.text = li.SIS.password
            self.ids.SIS_use.active = li.SIS.use
            self.ids.LMS_username.text = li.LMS.username
            self.ids.LMS_password.text = li.LMS.password
            self.ids.LMS_use.active = li.LMS.use

    def resetCookieJar(self):
        """
        Doesn't actually reset cookiejar, it rather sets error flag to reset cookiejar.
        Cookiejar is a collection of web browser cookies.
        """
        self.hadError = True

    def tryLogin(self):
        """
        Called when Login button is pressed, it tries to login. It checks if user is already logging in, and if at least one of systems is selected
        """
        if self.ids.login.text == "Logging in":
            return
        if (not self.ids.SIS_use.active and not self.ids.LMS_use.active):
            self.ids.SIS_error.text = "You must select at least one system"
            self.ids.LMS_error.text = "You must select at least one system"
            return
        self.startLoggingIn()
        self.startLMSLogin()

    def updateFunction(self, dt=None):
        """
        Update status of a login by one
        """
        self.ids.login.value += 1.0

    def startLoggingIn(self):
        """
        Initializes GUI for logging in
        """
        LMS.reset()
        SIS.reset()
        self.ids.login.text = "Logging in"
        self.ids.login.blink = True
        self.ids.login.max = (int(self.ids.SIS_use.active) + int(self.ids.LMS_use.active)) * 2
        self.ids.login.value = 0
        self.ids.SIS_error.text = ""
        self.ids.LMS_error.text = ""
        self.hadError = False

    def finishLoggingIn(self):
        """
        Tells GUI that logging in is finished
        """
        self.ids.login.working = False
        self.ids.login.text = "Login"
        self.ids.login.value = self.ids.login.max
        if (self.hadError):
            LMS.cookiejar = None
            SIS.cookiejar = None
        else:
            from MainScreen import MainScreen
            LoginProvider.setLoginInformation(self.ids.SIS_username.text, self.ids.SIS_password.text, self.ids.SIS_use.active,
                                              self.ids.LMS_username.text, self.ids.LMS_password.text, self.ids.LMS_use.active)
            MainScreenManager.switch_to(MainScreen())
            MainScreenManager.remove_widget(self)


    def startSISLogin(self):
        """
        Starts SIS login. It also checks if SIS login checkbox is selected by user
        """
        self.ids.login.value = int(self.ids.LMS_use.active)*2
        li = LoginInfo(self.ids.SIS_username.text, self.ids.SIS_password.text, self.ids.SIS_use.active)
        if not li.use:
            self.finishLoggingIn()
            return
        print 'trying SIS'
        LoginProvider.isSISLoginInfoValid(li, self.gotSISResult, self.gotSISError, self.updateFunction)

    def gotSISResult(self, dt):
        """
        This function is called when SIS login was successful
        """
        print "SIS login valid"
        self.finishLoggingIn()

    def gotSISError(self, e, dt):
        """
        This function is called when there was error during SIS login
        """
        print "SIS login invalid"
        self.ids.SIS_error.text = e
        self.resetCookieJar()
        self.finishLoggingIn()

    def startLMSLogin(self):
        """
        Starts LMS login. It also checks if LMS login checkbox is selected by user
        """
        li = LoginInfo(self.ids.LMS_username.text, self.ids.LMS_password.text, self.ids.LMS_use.active)
        if not li.use:
            self.startSISLogin()
            return
        print 'trying LMS'
        LoginProvider.isLMSLoginInfoValid(li, self.gotLMSResult, self.gotLMSError, self.updateFunction)
        
    def gotLMSResult(self, dt):
        """
        This function is called when LMS login was successful
        """
        print "LMS login valid"
        self.startSISLogin()

    def gotLMSError(self, e, dt):
        """
        This function is called when there was error during LMS login
        """
        print "LMS login invalid"
        self.ids.LMS_error.text = e
        self.resetCookieJar()
        self.startSISLogin()