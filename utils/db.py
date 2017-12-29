# -*- coding: utf-8 -*-
import json
from collections import OrderedDict, namedtuple

import aioodbc
from core.config import config

user_task_nt = namedtuple('user_task', 'id name state args')
active_task_nt = namedtuple('active_task', 'id name tg_id args')


class Users(object):
    @staticmethod
    async def get_user_info(user_id):
        cur = await db.cursor()
        await cur.execute("SELECT id, name, tg_id FROM users WHERE tg_id=?", user_id)
        res = await cur.fetchone()
        await cur.close()
        if not res:
            return
        user = {'id': res[0], 'name': res[1], 'tg_id': res[2]}
        tasks = await Tasks.get_user_tasks(user['id'])
        user['tasks'] = tasks
        return user

    @staticmethod
    async def add_user(name, tg_id):
        cur = await db.cursor()
        await cur.execute("INSERT INTO users(name, tg_id) VALUES(?, ?)", name, tg_id)
        if not cur.rowcount:
            await cur.close()
            raise Exception("Error inserting user")
        await cur.commit()
        await cur.close()
        return await Users.get_user_info(tg_id)


class Tasks(object):
    @staticmethod
    async def get_user_tasks(user_id, only_active=True):
        cur = await db.cursor()
        only_active_filter = " AND state = 1" if only_active else ''
        await cur.execute("SELECT id, name, state, args from tasks WHERE user_id = ?" + only_active_filter + " ORDER BY id", user_id)
        res = await cur.fetchall()
        await cur.close()
        tasks = OrderedDict()
        for item in res:
            task = user_task_nt(*item[:3], json.loads(item[3]))
            tasks[task.name] = task
        return tasks

    @staticmethod
    async def get_active_tasks():
        cur = await db.cursor()
        await cur.execute("SELECT t.name, u.tg_id, t.args from tasks t JOIN users u ON u.id = t.user_id WHERE state = 1")
        res = await cur.fetchall()
        await cur.close()
        tasks = []
        for item in res:
            task = active_task_nt(*item[:2], json.loads(item[2]))
            tasks.append(task)
        return tasks

    @staticmethod
    async def add_new_task(user_id, name, **kwargs):
        cur = await db.cursor()
        args = json.dumps(kwargs)
        await cur.execute("INSERT INTO tasks(name, user_id, state, args) VALUES(?, ?, 1, ?)", name, user_id, args)
        if not cur.rowcount:
            await cur.close()
            raise Exception("Error inserting task")
        await cur.commit()
        await cur.execute("SELECT id FROM tasks WHERE name=? AND user_id=?", name, user_id)
        res = await cur.fetchone()
        task_id = res[0]
        await cur.close()
        return user_task_nt(task_id, name, 1, kwargs)

    @staticmethod
    async def update_task(task_id, state):
        cur = await db.cursor()
        await cur.execute("UPDATE tasks SET state=? WHERE id=?", state, task_id)
        if not cur.rowcount:
            await cur.close()
            raise Exception("Error disabling task")
        await cur.commit()
        await cur.close()

    @staticmethod
    async def delete_task(task_id):
        cur = await db.cursor()
        await cur.execute("DELETE FROM tasks WHERE id=?", task_id)
        if not cur.rowcount:
            await cur.close()
            raise Exception("Error deleting task")
        await cur.commit()
        await cur.close()


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
