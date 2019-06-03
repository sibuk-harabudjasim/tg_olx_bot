# -*- coding: utf-8 -*-
import re
from bot.conversation.constants import States, mainmenu, Constants
from bot.userstor import with_user_data
from core.signal import start_task
from utils import log
from utils.common import detect_host, is_allowed_host
from utils.db import Tasks
from utils.markups import parse_list
from utils.validation import validate_url, validate_blacklist, validate_whitelist, validate_name


@with_user_data
def add_task(chat, *args, user_data):
    user_data['new_watch'] = {}
    user_data['state'] = States.ADD_TASK_URL
    return chat.send_text('Great! I will need URL, and two lists of words: whitelist and blacklist.\nLet`s start with URL, type it right now!')


def process_url(chat, message, user_data):
    url = validate_url(message['text'])
    if not url:
        return chat.send_text('Oops! Looks like url you typed does not correct. Please, try again.')
    host = detect_host(url)
    if not is_allowed_host(host):
        return chat.send_text('Oops! I don`t know how to handle this site, for now I can parse only {}. Please, try another link.'.format(Constants.get_allowed_sites()))
    user_data['new_watch']['url'] = url
    user_data['new_watch']['type'] = host
    user_data['state'] = States.ADD_TASK_BLACKLIST
    return chat.send_text('Accepted! Now write down words you DON`T want to see in advert. Comma separated, like:\nboring, stupid, broken\nYou can even write part of words or couples, but don`t forget about commas!')


def process_blacklist(chat, message, user_data):
    if re.findall(r"it['`]?s okay", message['text']):
        return goto_whitelist('Okay, it`s your choice.', chat, user_data)
    words = parse_list(message['text'])
    user_data['new_watch']['blacklist'] = words
    corr = validate_blacklist(words)
    if corr:
        return chat.send_text('If you don`t mind, I`d like to give you a little advice.' + ' '.join(corr) + ' You can retype your list right now, or just say "it\'s okay", I won`t stand on this.')
    return goto_whitelist('You`re doing well!', chat, user_data)


def goto_whitelist(prepend_message, chat, user_data):
    msg = 'Now write down words you WANT to see in advert. Comma separated, like:\nsuper, amazing, best\nYou can even write part of words or couples, but don`t forget about commas!'
    user_data['state'] = States.ADD_TASK_WHITELIST
    return chat.send_text(prepend_message + ' ' + msg)


def process_whitelist(chat, message, user_data):
    if re.findall(r"it['`]?s okay", message['text'], re.I):
        return goto_name('Okay, it`s your choice.', chat, user_data)
    words = parse_list(message['text'])
    user_data['new_watch']['whitelist'] = words
    corr = validate_whitelist(words)
    if corr:
        return chat.send_text('If you don`t mind, I`d like to give you a little advice.' + ' '.join(corr) + ' You can retype your list right now, or just say "it\'s okay", I won`t stand on this.')
    return goto_name('Seems good to me.', chat, user_data)


def goto_name(prepend_message, chat, user_data):
    msg = 'Last step to our success: name your subscription, so you can find and edit it later, any word you want.'
    user_data['state'] = States.ADD_TASK_NAME
    return chat.send_text(prepend_message + ' ' + msg)


async def process_name(chat, message, user_data):
    name = await validate_name(message['text'])
    if not name:
        return chat.sent_text('I think I saw this name somewhere, please, select another one.')
    name_text = '{} - great name! '.format(message['text'])
    if name != message['text']:
        name_text = 'Is "{}" okay? I just cannot use that name you typed. Sorry. Anyway, you won`t need to type it again.\n'.format(name)
    try:
        task = await Tasks.add_new_task(user_data['id'], name, **user_data['new_watch'])
    except Exception as e:
        log.error('add_task() error: {}', str(e))
    del user_data['new_watch']
    del user_data['state']
    start_task.emit(user_data['tg_id'], task)
    user_data['tasks'][task.name] = task
    return chat.send_text(name_text + 'We`re done. Your task is set up. Soon you`ll start receiving results. If you want to do something else - just take bottom menu.', markup=mainmenu)

__author__ = 'manitou'
