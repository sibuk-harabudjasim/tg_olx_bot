# -*- coding: utf-8 -*-
from bot.conversation.constants import Buttons, States, Constants, inline_fallback
from bot.conversation.error import fallback, error_message
from .start import start
from .add_task import add_task, process_url, process_blacklist, process_whitelist, process_name
from .task_list import task_list, task_info, task_delete, task_restore
from .about import about_message


def init_dialogs(bot):
    # START
    bot.add_command('/start', start)

    # ADD WATCH SEQ
    bot.add_command(Buttons.ADD_WATCH, add_task)
    bot.add_state_handler(States.ADD_TASK_URL, process_url)
    bot.add_state_handler(States.ADD_TASK_BLACKLIST, process_blacklist)
    bot.add_state_handler(States.ADD_TASK_WHITELIST, process_whitelist)
    bot.add_state_handler(States.ADD_TASK_NAME, process_name)
    bot.add_callback(Constants.FALLBACK, fallback)

    # TASK LIST HANDLERS
    bot.add_command(Buttons.MY_WATCHES, task_list)
    bot.add_callback(Constants.TASK_INFO_REGEX, task_info)
    bot.add_callback(Constants.TASK_DELETE_REGEX, task_delete)
    bot.add_callback(Constants.TASK_RESTORE_REGEX, task_restore)

    # HOW IT WORKS
    bot.add_command(Buttons.HOW_IT_WORKS, about_message)

    # FALLBACK
    bot.add_default_state_handler(error_message)
    bot.add_inline(Buttons.FALLBACK, fallback)


__author__ = 'manitou'
