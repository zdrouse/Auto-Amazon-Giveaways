from selenium import webdriver
import time
import getpass
import logging

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-infobars')

class GiveAwayBot(object):
	def __init__(self):
		self.chromedriver = webdriver.Chrome('C:\Python27\selenium\webdriver\chromedriver.exe', chrome_options=chrome_options)
		self.email = None
		self.password = None

	def _nav_to_ga(self):
		self.chromedriver.get('https://www.amazon.com/ga/giveaways')

	def _login(self, init=True):

		def check_for_continue():
			if self.chromedriver.find_element_by_id('continue'):
				return True
			else:
				return False

		print('Logging into Amazon...')
		self.chromedriver.get('https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_custrec_signin&switch_account=')
		if init:
			self.email = raw_input('Enter your Amazon email address: ')
			self.password = getpass.getpass('Enter your Amazon password: ')
		email_input_box = self.chromedriver.find_element_by_name('email')
		email_input_box.send_keys(self.email)
		continue_check = check_for_continue()
		if continue_check is True:
			continue_button = self.chromedriver.find_element_by_id('continue')
			continue_button.click()
		else:
			pass
		password_input_box = self.chromedriver.find_element_by_name('password')
		password_input_box.send_keys(self.password)
		sign_in = self.chromedriver.find_element_by_id('signInSubmit')
		sign_in.click()
		self.chromedriver.implicitly_wait(30)
		self._nav_to_ga()

	def no_req_giveaways(self):
		no_req_label = self.chromedriver.find_element_by_class_name('giveawayParticipationInfoContainer')
		print no_req_label

def main():
	ga_bot = GiveAwayBot()
	ga_bot._login()
	ga_bot.no_req_giveaways()

if __name__ == '__main__':
	main()