# -*- coding: utf-8 -*-
import asyncpg
import json
from collections import OrderedDict, namedtuple
from functools import wraps
from core.config import config

user_task_nt = namedtuple('user_task', 'id name type state args')
active_task_nt = namedtuple('active_task', 'id name type tg_id args')


def with_cursor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'cursor' in kwargs:
            return await func(*args, **kwargs)
        async with db.cursor() as cur:
            kwargs['cursor'] = cur
            return await func(*args, **kwargs)
    return wrapper


class Users(object):
    @staticmethod
    @with_cursor
    async def get_user_info(user_id, cursor=None):
        res = await cursor.fetchrow("SELECT id, name, tg_id FROM users WHERE tg_id=$1", user_id)
        if not res:
            return
        user = dict(res)
        tasks = await Tasks.get_user_tasks(user['id'], cursor=cursor)
        user['tasks'] = tasks
        return user

    @staticmethod
    @with_cursor
    async def add_user(name, tg_id, cursor=None):
        await cursor.execute("INSERT INTO users(name, tg_id) VALUES($1, $2)", name, tg_id)
        return await Users.get_user_info(tg_id, cursor=cursor)


class Tasks(object):
    @staticmethod
    @with_cursor
    async def get_user_tasks(user_id, only_active=True, cursor=None):
        only_active_filter = " AND state = 1" if only_active else ''
        res = await cursor.fetch("SELECT id, name, type, state, args from tasks WHERE user_id = $1" + only_active_filter + " ORDER BY id", user_id)
        tasks = OrderedDict()
        for item in res:
            task = user_task_nt(*tuple(item)[:-1], json.loads(item['args']))
            tasks[task.name] = task
        return tasks

    @staticmethod
    @with_cursor
    async def get_pending_tasks(cursor=None):
        res = await cursor.fetch(
            ("SELECT t.id, t.name, t.type, u.tg_id, t.args from tasks t JOIN users u ON u.id = t.user_id "
             "WHERE state = 1 AND t.start_time IS NOT NULL AND t.start_time < NOW()"))
        tasks = []
        for item in res:
            task = active_task_nt(*tuple(item)[:-1], json.loads(item['args']))
            tasks.append(task)
        return tasks

    @staticmethod
    @with_cursor
    async def add_new_task(user_id, name, type, **kwargs):
        cursor = kwargs.pop('cursor')
        args = json.dumps(kwargs)
        await cursor.execute("INSERT INTO tasks(name, type, user_id, state, args) VALUES($1, $2, $3, 1, $4)", name, type, user_id, args)
        task_id = await cursor.fetchval("SELECT id FROM tasks WHERE name=$1 AND user_id=$2", name, user_id)
        return user_task_nt(task_id, name, type, 1, kwargs)

    @staticmethod
    @with_cursor
    async def update_task(task_id, **kwargs):
        cursor = kwargs.pop('cursor')
        set_chunk = ', '.join(['{}=${}'.format(k, i + 2) for i, k in enumerate(kwargs)])
        await cursor.execute("UPDATE tasks SET {} WHERE id=$1".format(set_chunk), task_id, *kwargs.values())

    @staticmethod
    @with_cursor
    async def delete_task(task_id, cursor=None):
        await cursor.execute("DELETE FROM tasks WHERE id=$1", task_id)

    @staticmethod
    @with_cursor
    async def get_all_task_names(cursor=None):
        res = await cursor.fetch(
            "SELECT name from tasks WHERE state = 1")
        return [t['name'] for t in res]


class DbCursor(object):
    conn = None

    def __init__(self, db):
        self.db = db

    async def __aenter__(self):
        if not self.db.ready:
            await self.db.init()
        if not self.conn:
            try:
                self.conn = await self.db.pool.acquire()
            except Exception as e:
                print('DB error {}', str(e))
                raise
        return self.conn

    async def __aexit__(self, *args):
        if self.conn:
            conn, self.conn = self.conn, None
            return await self.db.pool.release(conn)


class DB(object):
    pool = None

    async def init(self):
        if self.pool:
            return
        self.pool = await asyncpg.create_pool(dsn=config.DATABASE_URL)

    def cursor(self):
        return DbCursor(self)

    @property
    def ready(self):
        return bool(self.pool)


db = DB()


__author__ = 'manitou'
