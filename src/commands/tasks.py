import resources
import util


@util.listenerfinder.register
class GreetNewMember(util.Listener):

    def __init__(self):
        super().__init__()

    async def on_member_join(self, member):
        await self.client.send_message(member.server.default_channel, resources.GREET_NEW_MEMBER.format(member=member))