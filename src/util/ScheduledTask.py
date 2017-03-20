from util import Listener


class ScheduledTask(Listener):
    """
    A task that is started once the bot is connected to Discord.
    """

    async def on_start(self):
        self.client.loop.create_task(self.task())

    async def task(self):
        """
        The coroutine that is to be run.
        """
        pass
