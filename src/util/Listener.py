import logging

import discord

from . import ListenerRegistry


class Help:
    def __init__(self, category='', title='', desc=''):
        self.category = category
        self.title = title
        self.desc = desc


class Listener:
    """
    Listens to events that may fire from the ListenerRegistry. Provides stub methods that should be extended.
    """

    def __init__(self):
        self._registry = None

    @property
    def registry(self) -> ListenerRegistry:
        """
        The registry that this is attached to
        :return: The registry, or None if not registered
        """
        return self._registry

    @registry.setter
    def registry(self, registry: ListenerRegistry):
        self._registry = registry

    @property
    def client(self) -> discord.Client:
        """
        The client to use
        :return: The client, or None if not attached to a registry
        """
        return None if self.registry is None else self.registry.client

    def is_triggered_message(self, msg: discord.Message) -> bool:
        """
        Is it triggered by a message, public or private?
        @param msg: the message
        :return: is it triggered?
        """
        return False

    def is_triggered_private_message(self, msg: discord.Message) -> bool:
        """
        Is it triggered by a private message and ONLY a private message?
        :param msg: the message
        :return: is it triggered?
        """
        return False

    async def on_pre_load(self):
        """
        Tasks to perform before the client has even started
        """
        pass

    async def on_start(self):
        """
        When the client is started
        """
        pass

    async def on_message(self, msg: discord.Message):
        """
        When triggered by a message, public or private
        :param msg: the message
        """
        pass

    async def on_private_message(self, msg: discord.Message):
        """
        When triggered by private messages
        :param msg: the message
        :return:
        """
        pass

    async def on_member_join(self, member):
        pass

    def overrides_mute(self) -> bool:
        """
        Will a muted user still be able to trigger this?
        :return: if the user can trigger
        """
        return False

    def get_help(self, msg) -> Help:
        """
        What will be displayed for this command if someone pm's the bot "help".
        :return: A help object, or None if it is not to be displayed
        """
        return None
