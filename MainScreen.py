from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from login import LoginProvider
import SIS
import LMS
from common import MainScreenManager

class MainScreen(Screen):
    def __init__(self):
        Screen.__init__(self, name="main")
        li = LoginProvider.getLoginInformation()
        if li.SIS.use:
            LoginProvider.isSISLoginInfoValid(li.SIS, self.gotSIS, self.errorSIS)
        else:
            self.errorSIS(None)
        if li.LMS.use:
            LoginProvider.isLMSLoginInfoValid(li.LMS, self.gotLMS, self.errorLMS)
        else:
            self.errorLMS(None)
            
    def gotSIS(self, dt = None):
        SIS.SISBrowser(self.gotSISData).getUserInfo()
        pass
        
    def errorSIS(self, e = None, dt = None):
        if e == 'User already logged in. Try logging out first':
            self.gotSIS()
        
    def gotSISData(self, dt = None):
        self.ids.SISName.text = SIS.SISData.namesurname
        self.ids.SISID.text = SIS.SISData.studentID
        self.ids.SISDepartment.text = SIS.SISData.department
        self.ids.SISEmail.text = SIS.SISData.eMail
        
    def gotLMS(self, dt = None):
        pass
        
    def errorLMS(self, e, dt = None):
        pass
        
    def logout(self):
        from LoginScreen import LoginScreen
        MainScreenManager.switch_to(LoginScreen())
        MainScreenManager.remove_widget(self)