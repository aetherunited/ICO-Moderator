import re

import discord

from .Listener import Listener, Help


class BasicTextCommand(Listener):
    """
    A simple text command, to be only used for the simplest of emotes
    """

    def get_command_name(self) -> str:
        """
        The regex to use that triggers the command
        :return: a regex string
        """
        return r''

    def get_response(self) -> str:
        """
        A string to respond to a command with.

        Format table to be used:
         - message: the message that triggered the command
         - author: the author that wrote the message
         - channel: the channel the message was in
        :return: a string
        """
        return ''

    def get_format_table(self) -> dict:
        """
        A format table to be added to the existing one
        :return: a dictionary referencing string to string
        """
        return {}

    def get_category(self) -> str:
        """
        The category to be displayed in the help.
        :return: the name of the category
        """
        return 'Emotes'

    def is_triggered_message(self, msg: discord.Message):
        return re.search(self.get_command_name(), msg.content) is not None

    def _build_msg(self, msg):
        format_table = {
            'message': msg,
            'author': msg.author,
            'channel': msg.channel,
            **self.get_format_table()
        }
        return self.get_response().format(**format_table)

    async def on_message(self, msg: discord.Message):
        await self.client.send_message(msg.channel, self._build_msg(msg))

    def get_help(self, msg):
        return Help(self.get_category(), self.get_command_name(), self._build_msg(msg))