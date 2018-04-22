import asyncio
from pyppeteer import launch
import getpass
import logging

class GiveAwayPrize(object):
    def __init__(self):
        self.prize_name = None
        self.prize_req = None
        self.prize_url = None
        self.prize_entry = None

    def set_prize_name(self, prize_name):
        self.prize_name = prize_name

    def set_prize_req(self, prize_req):
        self.prize_req = prize_req

    def set_prize_url(self, prize_url):
        self.prize_url = prize_url
    
    def get_prize_name(self):
        return self.prize_name

    def get_prize_req(self):
        return self.prize_req
    
    def get_prize_url(self):
        return self.prize_url
