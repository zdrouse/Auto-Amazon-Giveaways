import asyncio
from pyppeteer import launch
import time
import getpass
import logging

class GiveAwayBot(object):
	def __init__(self):
		self.email = None
		self.password = None
		self.browser = None

	async def _nav_to_ga(self):
		self.browser= await launch()
		page = await self.browser.newPage()
		await page.goto('https://www.amazon.com/ga/giveaways')
		return page

	async def _login(self, init=True):

		async def get_browser():
			return await launch(headless=False)

		def check_for_continue():
			if self.chromedriver.find_element_by_id('continue'):
				return True
			else:
				return False

		print('Logging into Amazon...')
		if init:
			self.email = input('Enter your Amazon email address: ')
			self.password = getpass.getpass('Enter your Amazon password: ')
		self.browser = await get_browser()
		login_page = await self.browser.newPage()
		await login_page.goto('https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fgiveaway%2Fhome%2Fref%3Dnav_custrec_signin&switch_account=')
		email_input_box = '#ap_email'
		await login_page.type(email_input_box, self.email)
		continue_button = '#continue'
		await login_page.click(continue_button)
		password_input_box = '#ap_password'
		remember_me = '#rememberMe'
		sign_in_button = '#signInSubmit'
		await login_page.waitForSelector(password_input_box, timeout=30000)
		await login_page.type(password_input_box, self.password)
		#await login_page.click(remember_me)
		await login_page.click(sign_in_button)
		print(email_input_box)
		print(continue_button)
		await asyncio.sleep(10)
		#await self.browser.close()
		#self._nav_to_ga()

	def no_req_giveaways(self):
		no_req_label = self.chromedriver.find_element_by_class_name('giveawayParticipationInfoContainer')
		print(no_req_label)

async def main():
	ga_bot = GiveAwayBot()
	await ga_bot._login()
	#ga_bot.no_req_giveaways()

asyncio.get_event_loop().run_until_complete(main())