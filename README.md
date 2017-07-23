# ICO Moderator

A moderator for Ethereum ICOs using Discord as a communications platform. It acts as a _safeguard_ against possible phishing scammers on your server, cannot completely prevent all phishing scams. [Click here to add the bot to your server.](https://discordapp.com/oauth2/authorize?client_id=338442093892468736&scope=bot&permissions=11264) 

##Usage

- Whenever someone posts a URL listed on the [blacklist found here](https://raw.githubusercontent.com/MyEtherWallet/ethereum-lists/master/urls-darklist.json), or any link that redirects to the blacklist including most URL shorteners,, the bot will delete the message.
- Whenever someone posts a 40-digit hexadecimal string (in other words, an Ethereum address), that message will be deleted unless the person is part of a role named `addressannouncer`.

---
_Donations are welcome at my Ethereum address:_ `0xD2Cb35e82180FFCE90D2617703a19A23DF7A4b08`
