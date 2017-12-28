# -*- coding: utf-8 -*-
import aioodbc
from core.config import config


class Users(object):
    @staticmethod
    async def get_user_info(user_id):
        print('==============get user info', user_id)
        cur = await db.cursor()
        await cur.execute("SELECT id, name, tg_id FROM users WHERE tg_id=?", user_id)
        res = await cur.fetchone()
        if not res:
            print('=============no user')
            return
        return {'id': res[0], 'name': res[1], 'tg_id': res[2]}

    @staticmethod
    async def add_user(name, tg_id):
        print('==============add user', name, tg_id)
        cur = await db.cursor()
        await cur.execute("INSERT INTO users(name, tg_id) VALUES(?, ?)", name, tg_id)
        if not cur.rowcount:
            print('================error inserting')
            raise Exception("Error inserting user")
        print('===================user done')
        return {'id': None, 'name': name, 'tg_id': tg_id}


class Tasks(object):
    @staticmethod
    async def get_user_tasks(user_id, only_active=True):
        cur = await db.cursor()
        only_active_filter = " AND state = 1" if only_active else ''
        await cur.execute("SELECT * from tasks WHERE user_id = ?" + only_active_filter, user_id)
        res = await cur.fetchall()
        # TODO: process tasks
        return res

    @staticmethod
    async def get_active_tasks():
        cur = await db.cursor()
        await cur.execute("SELECT * from tasks WHERE state = 1")
        res = await cur.fetchall()
        # TODO: process tasks
        return res


class DB(object):
    _conn = None

    async def init(self):
        if self._conn:
            return
        self._conn = await aioodbc.connect(dsn=config.DB_DSN, echo=config.DEBUG)

    async def cursor(self):
        if not self._conn:
            await self.init()
        return await self._conn.cursor()


db = DB()


__author__ = 'manitou'
