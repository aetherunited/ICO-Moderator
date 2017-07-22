"""
The memes storage file
"""

CONFUCIUS = '127889357079183360'

RYAN = '164573486340112384'
JZ = '124016824202297344'

ETH_WHITELIST = [
    #CONFUCIUS,
    RYAN,
    JZ
]

URL = 'https://discordapp.com/oauth2/authorize?&client_id={bot_id}&scope={scope}&permissions={permissions}'

GREET_NEW_MEMBER = 'Hello, {member.mention}, and welcome to Aether United!'

if __name__ == '__main__':
    print(globals())
