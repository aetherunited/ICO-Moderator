# ICO Moderator

A moderator for Ethereum ICOs using Discord as a communications platform. It acts as a _safeguard_ against possible phishers on your server, but cannot completely prevent all phishers. [Click here to add the bot to your server.](https://discordapp.com/oauth2/authorize?client_id=338442093892468736&scope=bot&permissions=11264) 

## Usage

- Whenever someone posts a URL listed on [this blacklist](https://raw.githubusercontent.com/MyEtherWallet/ethereum-lists/master/urls-darklist.json), the message will be removed. Also, any link that redirects you to the blacklist (including most URL shorteners*), will also get deleted. Even if the redirect chain is something convoluted, like `tinyurl.com -> bit.ly -> goo.gl -> fishy-looking.website`, it will still get deleted.
- Whenever someone posts a 40-digit hexadecimal string (in other words, an Ethereum address), that message will also be deleted. To whitelist someone and allow them to post an address, you must create a role called `AddressAnnouncer` (case insensitive) and add that person to the role. 

<sub>_*Known exceptions to this: [donotlink.it](https://donotlink.it)_</sub>

---

_Donations are welcome at my Ethereum address:_ `0xD2Cb35e82180FFCE90D2617703a19A23DF7A4b08`

This software is licensed under the _GNU AGPLv3 License.
