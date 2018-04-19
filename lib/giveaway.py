import asyncio
from pyppeteer import launch
import getpass
import logging

class GiveAwayBot(object):
	def __init__(self):
		self.email = None
		self.password = None
		self.browser = None

	async def _nav_to_ga(self, login_page):
		ga_page = await login_page.goto('https://www.amazon.com/ga/giveaways')
		return ga_page

	async def login(self, init=True):
		email_input_box = '#ap_email'
		password_input_box = '#ap_password'
		remember_me = '#rememberMe'
		sign_in_button = '#signInSubmit'

		async def get_browser():
			return await launch(headless=False)

		async def check_for_continue(login_page):
			continue_button = '#continue'
			is_continue_present = await login_page.querySelector(continue_button)
			if is_continue_present:
				await login_page.click(continue_button)
			else:
				pass

		print('Logging into Amazon...')
		if init:
			self.email = input('Enter your Amazon email address: ')
			self.password = getpass.getpass('Enter your Amazon password: ')
		self.browser = await get_browser()
		login_page = await self.browser.newPage()
		await login_page.setViewport({'width': 1800, 'height': 1000})
		await login_page.goto('https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fgiveaway%2Fhome%2Fref%3Dnav_custrec_signin&switch_account=')
		await login_page.type(email_input_box, self.email)
		await check_for_continue(login_page)
		await login_page.waitForSelector(password_input_box, timeout=5000)
		await login_page.type(password_input_box, self.password)
		#await self.browser.click(remember_me)
		await login_page.click(sign_in_button)
		print(email_input_box)
		await asyncio.sleep(2)
		# this will navigate to root Giveaway page after successful login and return the page.
		await self._nav_to_ga(login_page)
		await asyncio.sleep(15)
		#await self.browser.close()

	async def no_req_giveaways(self, ga_page):
		no_req_label = '#giveawayParticipationInfoContainer'
		is_label = await ga_page.querySelector(no_req_label)
		if is_label:
			print(is_label + ' found')
		else:
			print(is_label)

async def main():
	ga_bot = GiveAwayBot()
	ga_page = await ga_bot.login()
	await ga_bot.no_req_giveaways(ga_page)

asyncio.get_event_loop().run_until_complete(main())