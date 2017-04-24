import logging
import yaml
import re
import time
import string

import asyncio
import discord
import util


MSGS_SINCE_LAST = 10
MINS_SINCE_LAST = 10

_logger = logging.getLogger('qa')


class DictionaryDot:
    """
    Example usage:
    >>> DictionaryDot({'asdf': 123}).asdf
    123
    """
    def __init__(self, data):
        self.data = data

    def __getattr__(self, index):
        return self.data[index]


class Subject:

    def __init__(self, subject, identifier, **responses):
        self.name = subject
        self.identifier = identifier.format(keywords=KEYWORDS)
        self.questions = [
            Question(subject, response, *q_types.split()) for q_types, response in responses.items()
        ]

    def __repr__(self):
        return 'Subject({})'.format(self.name)

    def get_question(self, q_type):
        for q in self.questions:
            if q_type in q.q_types:
                return q
        return None


class Question:

    def __init__(self, subject, response, *q_types):
        self.subject = subject
        self.q_types = q_types
        self.response = response

        self.last_queried = 0
        self.msgs_since_last = MSGS_SINCE_LAST

    def __repr__(self):
        return 'Question({}, {})'.format(self.subject, self.q_types)

    def update_msgs_since(self):
        self.msgs_since_last += 1

    def set_last_queried(self):
        self.last_queried = time.time()

    def can_respond(self):
        return time.time() > self.last_queried + 60*MINS_SINCE_LAST and self.msgs_since_last >= MSGS_SINCE_LAST


with open('res/questions.yaml') as f:
    raw_data = yaml.load(f.read())

    KEYWORDS = DictionaryDot({
        k: '(?:{b}(?:{keywords}){b})'.format(keywords='|'.join(map(lambda w: w, v)), b=r'\b')
        for k, v in raw_data['keywords'].items()
    })

    subjs = raw_data['subjects']
    SUBJECTS = {
        name: Subject(name, subjs[name]['identifier'], **subj['responses']) for (name, subj) in subjs.items()
    }

QUESTION_REGEX = r'(?i)^(who|what|where|when|why|how|can).*?|$'


@util.listenerfinder.register
class QuestionAnswer(util.Listener):

    async def on_start(self):
        _logger.info('Subjects found: %s', ', '.join(SUBJECTS))
        print(list((s.name, s.identifier) for n, s in SUBJECTS.items()))

    def is_triggered_message(self, msg: discord.Message):
        return True

    async def on_message(self, msg: discord.Message):
        update_questions()

        found_question, q_type = contains_question(msg.content)

        if not found_question:
            _logger.debug('msg did not contain question, abort')
            return

        subj_match_pack = ((s, re.search(s.identifier, msg.content)) for n, s in SUBJECTS.items())
        matching_subjs = ((s, m) for s, m in subj_match_pack if m is not None)

        try:
            longest_match_pair = max(matching_subjs, key=lambda p: len(p[1].group()))
        except ValueError:
            _logger.debug('msg question did not contain subjects, aborting.')
            return

        subj, match = longest_match_pair

        if match:
            _logger.info('Found question about subject %s in message: %s', subj, msg.content)
            _logger.debug('Match group: %s', match.group())
            if subj:
                _logger.debug('%s exists', subj)
                question = subj.get_question(q_type)
                if question:
                    if question.can_respond():
                        _logger.debug('Question %s exists for %s', q_type, subj)
                        _logger.info('Sending message')
                        await self.client.send_typing(msg.channel)
                        await asyncio.sleep(0.5)
                        await self.client.send_message(msg.channel, question.response)
                        question.set_last_queried()
                    else:
                        _logger.info('Response to %s exists for %s, but not allowed to respond due to frequency, '
                                     'ignoring', q_type, subj)
                else:
                    _logger.info('%s exists, but does not have question %s, ignoring', subj, q_type)
            else:
                _logger.info("Subject '%s' does not exist, ignoring", subj)


def update_questions():
    for s in SUBJECTS:
        for q in SUBJECTS[s].questions:
            q.update_msgs_since()

def msg_to_sentences(msg):
    return re.split('[.?!:] *', msg)


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


if __name__ == '__main__':
    from pprint import pprint
    pprint(SUBJECTS['crowdsale'].questions)
