import discord
import re

import util


SWEARS = 'fuck shit cunt bitch dick asshole'.split()


def censor(word):
    return word[0] + '\\*' * (len(word)-2) + word[-1]


@util.listenerfinder.register
class SwearListener(util.Listener):

    def is_triggered_message(self, msg: discord.Message):
        return any(s in msg.content for s in SWEARS)

    async def on_message(self, msg: discord.Message):
        await self.client.delete_message(msg)
        output = msg.content
        for s in SWEARS:
            output = output.replace(s, censor(s))
        await self.client.send_message(msg.channel, '{} sent message: {}'.format(msg.author.mention, output))
        modlog = msg.server.get_channel('modlog')
        if modlog is not None:
            await self.client.send_message(modlog, '**Message sent by {} deleted:**\n{}'.format(msg.author.mention, msg.content))
