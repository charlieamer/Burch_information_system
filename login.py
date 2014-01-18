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

class LoginScreen(Screen):
	def tryLogin(self):
		self.ids.login.text = "Logging in"
		self.ids.login.max = 69000
		self.ids.login.value = -1
		LoginProvider.isSISLoginInfoValid(None, self.gotSISResult, self.gotError, self.updateProgress)
		self.prag = 0.0
	def updateProgress(self, thread, a, b):
		if b != -1:
			self.ids.login.max = b
		self.ids.login.value = a
	def gotSISResult(self, valid):
		self.ids.login.value = -1
		print "SIS Valid:",valid
		LoginProvider.isSISLoginInfoValid(None, self.gotLMSResult, self.gotError, self.updateProgress)
	def gotLMSResult(self, valid):
		print "LMS Valid:",valid
		self.ids.login.text = "Login"
	def gotError(self, e):
		print e
	
	
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
		
		def isSISLoginInfoValid(self, LoginInfo, resultFunction, errorFunction = None, progressFunction = None):
			self.resultFunction = resultFunction
			req = UrlRequest("http://lms.ibu.edu.ba/", on_success = self.isValid, on_error = errorFunction, on_progress = progressFunction )
		def isLMSLoginInfoValid(self, LoginInfo, resultFunction, errorFunction = None, progressFunction = None):
			self.resultFunction = resultFunction
			req = UrlRequest("https://my.ibu.edu.ba/", on_success = self.isValid, on_error = errorFunction, on_progress = progressFunction )
			
	instance = None
	def __init__(self):
		if (_LoginProvider.instance == None):
			_LoginProvider.instance = _LoginProvider.LoginSingleton()
		else:
			print 'LoginProvider already exists'

LoginProvider = _LoginProvider().instance