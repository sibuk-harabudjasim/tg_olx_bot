# -*- coding: utf-8 -*-
from bot.conversation import inline_fallback
from bot.userstor import with_user_data


@with_user_data
async def fallback(chat, cq, match, user_data):
    user_data.pop('state', None)
    await cq.answer()
    return await chat.edit_text(chat.message['message_id'], 'Sorry for that. So, what do you want to do now?')


def error_message(chat, message, user_data):
    if 'state' not in user_data:
        return chat.send_text('Please, use keyboard or buttons under message, it`s easier to navigate with them.')

    return chat.send_text('Oops! Something went wrong, for now we can start again and see how it goes', reply_markup=inline_fallback)


__author__ = 'manitou'
