import logging
import json
import re

import asyncio
import discord
import util


_logger = logging.getLogger('qa')


with open('res/questions.json') as f:
    DATA = json.loads(f.read())
    for k, v in DATA['subjects'].items():
        v['identifier'] = v['identifier'].format(**DATA['res'])

QUESTION_REGEX = r'(?i)^(who|what|where|when|why|how).*?|$'


@util.listenerfinder.register
class QuestionAnswer(util.Listener):

    def is_triggered_message(self, msg: discord.Message):
        return contains_question(msg.content)

    async def on_message(self, msg: discord.Message):
        subject, match, q_type = match_subject(msg.content)
        if match:
            _logger.info('Found question about subject %s in message: %s', subject, msg.content)
            _logger.debug('Match group: %s', match.group())
            response = DATA['subjects'][subject]['responses'].get(q_type)
            if response:
                await self.client.send_typing(msg.channel)
                await asyncio.sleep(0.5)
                await self.client.send_message(msg.channel, response)
            else:
                _logger.info("No response found for q_type '%s' of subject '%s'", q_type, subject)


def msg_to_sentences(msg):
    return re.split('[.?!] ', msg)


def is_question(sentence):
    match = re.search(QUESTION_REGEX, sentence)
    if match:
        try:
            return match.group(1).lower()
        except AttributeError:
            return False
    return False


def contains_question(msg):
    for sent in msg_to_sentences(msg):
        q_type = is_question(sent)
        if q_type:
            return sent, q_type
    return False, None


def match_subject(msg):
    question, q_type = contains_question(msg)
    if not question:
        return None, None, None
    packed = map(lambda k: (k, re.search(DATA['subjects'][k]['identifier'], question)), DATA['subjects'])
    filtered_keys = filter(lambda p: p[1] is not None, packed)
    try:
        return (*max(filtered_keys, key=lambda x: len(x[0])), q_type)
    except ValueError:
        return None, None, q_type


if __name__ == '__main__':
    from pprint import pprint
    pprint(DATA['subjects'])
