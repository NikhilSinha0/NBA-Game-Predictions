import time
import re

class settings:
    def __init__(self):
        self.delay = 0
        self.denyList = []

    def set_delay(self, seconds):
        self.delay = seconds

    def crawl_delay(self):
        time.sleep(self.delay)

    def add_to_denyList(self, item):
        self.denyList.append(item)

    def in_deny_list(self, item):
        for link in self.denyList: #will add regex support at a later time
            if(link in item):
                return True
        return False