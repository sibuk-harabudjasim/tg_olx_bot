# -*- coding: utf-8 -*-
from functools import wraps

from utils.db import Users


def with_user_data(fn):
    @wraps(fn)
    async def func(chat, *args, **kwargs):
        user_id, name = chat.sender['id'], chat.sender['first_name']
        user = await userstorage.get_or_create(name, user_id)
        return await fn(chat, *args, **kwargs, user_data=user)
    return func


class UserStorage(object):
    users = None

    def __init__(self):
        self.users = {}

    async def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        user = await Users.get_user_info(user_id)
        if not user:
            return
        self.users[user['tg_id']] = user
        return user

    async def add_user(self, name, user_id):
        user = await Users.add_user(name, user_id)
        self.users[user['tg_id']] = user
        return user

    async def get_or_create(self, name, user_id):
        user = await self.get_user(user_id)
        if not user:
            return await self.add_user(name, user_id)
        return user



userstorage = UserStorage()


__author__ = 'manitou'
