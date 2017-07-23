import asyncio
import logging
import re
import discord
import requests

import util

REDIRECT_LAYERS = 5
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
        # Cursory scan
        for blacklist_url in GetUrlsTask.blacklist:
            if re.search(r'\b{}\b'.format(blacklist_url), msg.content, flags=re.IGNORECASE):
                log.info('detected scam URL (%s) in message, deleting %s', blacklist_url, msg.content)
                return True

        # Deep scan
        for match in re.finditer(URL_REGEX, msg.content):
            url = match.string
            log.debug('deep scanning url %s', url)
            for _ in range(0, REDIRECT_LAYERS):
                try:
                    redirect = requests.head(match.string).headers.get('location')
                    if redirect is None:
                        log.debug('... does not redirect')
                        break
                    if any(blacklist in redirect for blacklist in blacklist_url):
                        log.info('... redirects to %s, a scam url', redirect)
                        return True
                    else:
                        log.debug('... redirects to %s', redirect)
                        url = redirect
                except ConnectionError:
                    log.debug('could not connect to %s, skipping', url)
                    break

        return False

    async def on_message(self, msg: discord.Message):
        await self.client.delete_message(msg)
        notice = await self.client.send_message(msg.channel, '_A message from {} that contained a suspicious URL was deleted._'.format(msg.author.mention))
        await asyncio.sleep(10)
        await self.client.delete_message(notice)
        return


@util.listenerfinder.register
class AddressDeletor(util.Listener):

    def is_triggered_message(self, msg: discord.Message):
        for role in msg.author.roles:
            if any(r.name.lower() == 'addressannouncer' for r in msg.author.roles):
                log.debug('message from person on crypto address whitelist, not moderating for addresses')
                return False
        if re.search(r'[0-9a-f]{38,45}', msg.content, flags=re.IGNORECASE):
            return True

    async def on_message(self, msg: discord.Message):
        log.info('detected potential scam address in message, deleting', msg.content)
        await self.client.delete_message(msg)
        notice = await self.client.send_message(msg.channel, '_A message from {} that contained an ethereum address was deleted._'.format(msg.author.mention))
        await asyncio.sleep(10)
        await self.client.delete_message(notice)
        return
