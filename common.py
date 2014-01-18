class LoginInfo:
	username = None
	password = None
	use = False
	def __init__(self, username, password, use):
		self.username = username
		self.password = password
		self.use = use