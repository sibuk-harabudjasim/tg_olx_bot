# -*- coding: utf-8 -*-
from bot.conversation.constants import Buttons, Constants
from bot.conversation.error import error_message
from bot.userstor import with_user_data, callback_with_user_data
from core.signal import stop_task, start_task
from utils import log
from utils.db import Tasks
from utils.markups import make_inline_keyboard


@with_user_data
def task_list(chat, *args, user_data):
    if not user_data['tasks']:
        return chat.send_text('You don`t have any. Try to add them using "{}" on keyboard.'.format(Buttons.ADD_WATCH))
    task_buttons = []
    for task in user_data['tasks'].values():
        task_buttons.append((task.name, Constants.TASK_INFO_TMPL.format(task.name)))
    tasks_keyboard = make_inline_keyboard(1, *task_buttons)
    return chat.send_text('Here`s your watches:', reply_markup=tasks_keyboard)


@callback_with_user_data
async def task_info(chat, cq, match, user_data):
    await cq.answer()
    task_name = match.group(1)
    if task_name not in user_data['tasks']:
        log.warning('Task name \'{}\' not in user tasks {}', task_name, user_data['tasks'].keys())
        log.debug('User data: {}', user_data)
        return await error_message(chat, None, user_data)
    task = user_data['tasks'][task_name]
    info = '''
        Task info:
        Name: {}
        State: {}
        URL: {}
        Blacklist: {}
        Whitelist: {}
    '''.format(
        task.name,
        'active' if task.state else 'inactive',
        task.args['url'],
        ', '.join(task.args['blacklist']),
        ', '.join(task.args['whitelist'])
    )
    delete_inline = make_inline_keyboard(1, (Buttons.TASK_DELETE, Constants.TASK_DELETE_TMPL.format(task_name)), to_json=False)
    return await chat.edit_text(chat.message['message_id'], info, markup=delete_inline)


@callback_with_user_data
async def task_delete(chat, cq, match, user_data):
    await cq.answer()
    task_name = match.group(1)
    if task_name not in user_data['tasks']:
        # TODO: replace with more precise message
        return await error_message(chat, None, user_data)
    task = user_data['tasks'][task_name]
    try:
        await Tasks.update_task(task.id, state=0)
    except Exception as e:
        # TODO: process exception
        pass
    del user_data['tasks'][task_name]
    stop_task.emit(task.id)
    restore_inline = make_inline_keyboard(1, (Buttons.TASK_RESTORE, Constants.TASK_RESTORE_TMPL.format(task.id)), to_json=False)
    return await chat.edit_text(chat.message['message_id'], 'Yep, it`s deleted now. But you can restore it if you want. Or just use keyboard below.', markup=restore_inline)


@callback_with_user_data
async def task_restore(chat, cq, match, user_data):
    await cq.answer()
    task_id = int(match.group(1))
    try:
        await Tasks.update_task(task_id, state=1)
    except Exception as e:
        # TODO: process exception
        pass
    user_data['tasks'] = await Tasks.get_user_tasks(user_data['id'])
    task = [t for t in user_data['tasks'].values() if t.id == task_id][0]
    start_task.emit(user_data['tg_id'], task)
    return await chat.edit_text(chat.message['message_id'], 'Done, let`s go to the keyboard below.')


__author__ = 'manitou'
