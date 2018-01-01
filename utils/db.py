# -*- coding: utf-8 -*-
import json
from collections import OrderedDict, namedtuple

import aiopg

from core.config import config

user_task_nt = namedtuple('user_task', 'id name type state args')
active_task_nt = namedtuple('active_task', 'id name type tg_id args')


class Users(object):
    @staticmethod
    async def get_user_info(user_id):
        async with db.cursor() as cur:
            await cur.execute("SELECT id, name, tg_id FROM users WHERE tg_id=%s", (user_id,))
            res = await cur.fetchone()
        if not res:
            return
        user = {'id': res[0], 'name': res[1], 'tg_id': res[2]}
        tasks = await Tasks.get_user_tasks(user['id'])
        user['tasks'] = tasks
        return user

    @staticmethod
    async def add_user(name, tg_id):
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO users(name, tg_id) VALUES(%s, %s)", (name, tg_id))
            if not cur.rowcount:
                raise Exception("Error inserting user")
        return await Users.get_user_info(tg_id)


class Tasks(object):
    @staticmethod
    async def get_user_tasks(user_id, only_active=True):
        async with db.cursor() as cur:
            only_active_filter = " AND state = 1" if only_active else ''
            await cur.execute("SELECT id, name, type, state, args from tasks WHERE user_id = %s" + only_active_filter + " ORDER BY id", (user_id,))
            res = await cur.fetchall()
        tasks = OrderedDict()
        for item in res:
            task = user_task_nt(*item)
            tasks[task.name] = task
        return tasks

    @staticmethod
    async def get_active_tasks():
        async with db.cursor() as cur:
            await cur.execute("SELECT t.id, t.name, t.type, u.tg_id, t.args from tasks t JOIN users u ON u.id = t.user_id WHERE state = 1")
            res = await cur.fetchall()
            tasks = []
            for item in res:
                task = active_task_nt(*item)
                tasks.append(task)
            return tasks

    @staticmethod
    async def add_new_task(user_id, name, type, **kwargs):
        async with db.cursor() as cur:
            args = json.dumps(kwargs)
            await cur.execute("INSERT INTO tasks(name, type, user_id, state, args) VALUES(%s, %s, %s, 1, %s)", (name, type, user_id, args))
            if not cur.rowcount:
                raise Exception("Error inserting task")
            await cur.execute("SELECT id FROM tasks WHERE name=%s AND user_id=%s", (name, user_id))
            res = await cur.fetchone()
            task_id = res[0]
            return user_task_nt(task_id, name, type, 1, kwargs)

    @staticmethod
    async def update_task(task_id, state):
        async with db.cursor() as cur:
            await cur.execute("UPDATE tasks SET state=%s WHERE id=%s", (state, task_id))
            if not cur.rowcount:
                raise Exception("Error disabling task")

    @staticmethod
    async def delete_task(task_id):
        async with db.cursor() as cur:
            await cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
            if not cur.rowcount:
                raise Exception("Error deleting task")

    @staticmethod
    async def get_all_task_names():
        async with db.cursor() as cur:
            await cur.execute(
                "SELECT name from tasks WHERE state = 1")
            res = await cur.fetchall()
            return [t[0] for t in res]


class DbCursor(object):
    pool = None
    conn = None
    cursor = None

    def __init__(self, db):
        self.db = db

    async def __aenter__(self):
        if not self.db.ready:
            await self.db.init()
        if not self.conn:
            try:
                self.conn = await self.db.pool.acquire()
            except Exception as e:
                print('EXCEPTION', str(e))
                raise
        if not self.cursor:
            try:
                self.cursor = await self.conn.cursor()
            except Exception as e:
                print('EXCEPTION', str(e))
                raise
        return self.cursor

    async def __aexit__(self, *args):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class DB(object):
    pool = None

    async def init(self):
        if self.pool:
            return
        self.pool = await aiopg.create_pool(dsn=config.DATABASE_URL, echo=config.DEBUG)

    def cursor(self):
        return DbCursor(self)

    @property
    def ready(self):
        return bool(self.pool)


db = DB()


__author__ = 'manitou'
