import kivy
import pickle
import sys
import LMS
import SIS
import os
   
class LoginInfo:
    username = None
    password = None
    use = False
    def __init__(self, username, password, use):
        self.username = username
        self.password = password
        self.use = use
        
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
                ret = None
            except:
                print "Unexpected error:", sys.exc_info()[1]
                ret = None
            return ret
            
        def writeLoginInformation(self, LoginInfo):
            try:
                pickle.dump(LoginInfo, open("data/loginInfo","wb"))
            except IOError as e:
                print "Error writing login file:", e.strerror
                
        def setLoginInformation(self, SISUsername, SISPassword, SISUse, LMSUsername, LMSPassword, LMSUse):
            info = LoginInformation()
            info.LMS = LoginInfo(LMSUsername, LMSPassword, LMSUse)
            info.SIS = LoginInfo(SISUsername, SISPassword, SISUse)
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