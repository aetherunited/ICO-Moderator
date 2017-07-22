import asyncio
import discord
import itertools
import requests
import json
from urllib.parse import urlparse
import logging
import re

import resources
import util

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
URL_SOURCE = 'https://raw.githubusercontent.com/MyEtherWallet/ethereum-lists/master/urls-darklist.json'
UPDATE_PERIOD = 3600  # Every hour

log = logging.getLogger(__name__)


@util.listenerfinder.register
class GetUrlsTask(util.ScheduledTask):

    blacklist = []

    async def task(self):
        while True:
            log.info('updating url blacklist...')
            response = requests.get(URL_SOURCE)
            content = response.content.decode()
            GetUrlsTask.blacklist = re.findall(r'"id": ?"(.+)"', content)  # because it errors with proper json.loads...
            log.debug('updated blacklist: ', GetUrlsTask.blacklist)
            await asyncio.sleep(UPDATE_PERIOD)


@util.listenerfinder.register
class URLModerator(util.Listener):

    def is_triggered_message(self, msg: discord.Message):
        for blacklist_url in GetUrlsTask.blacklist:
            if re.search(r'{}\b'.format(blacklist_url), msg.content, flags=re.IGNORECASE):
                return True

    async def on_message(self, msg: discord.Message):
        log.info('detected scam URL in message, deleting', msg.content)
        await self.client.delete_message(msg)
        notice = await self.client.send_message(msg.channel, '_A message that contained a suspicious URL was deleted._')
        await asyncio.sleep(10)
        await self.client.delete_message(notice)
        return


@util.listenerfinder.register
class AddressDeletor(util.Listener):

    def is_triggered_message(self, msg: discord.Message):
        if msg.author.id in resources.ETH_WHITELIST:
            log.debug('message from person on crypto address whitelist')
            return False
        if re.search(r'[0-9a-f]{38,45}', msg.content):
            return True

    async def on_message(self, msg: discord.Message):
        log.info('detected potential scam address in message, deleting', msg.content)
        await self.client.delete_message(msg)
        notice = await self.client.send_message(msg.channel, '_A message that contained a crypto address was deleted._')
        await asyncio.sleep(10)
        await self.client.delete_message(notice)
        return
