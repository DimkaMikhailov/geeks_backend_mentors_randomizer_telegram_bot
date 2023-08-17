from sqlite3 import Error
import sqlite3
from typing import Any, Dict

from config import db
from colorama import Fore
from datetime import datetime


class SQLOperator:
    def __init__(self):
        self.__con = None
        self.__cur = None

        self.__connect_db()

    def __connect_db(self):
        try:
            self.__con = sqlite3.connect(db)
            self.__cur = self.__con.cursor()
            print(f'{Fore.GREEN}database({db}): connect successfully{Fore.RESET}')
        except Error as e:
            print(e)

    def create_table(self, name, *args):
        table = f'''CREATE TABLE IF NOT EXISTS {name}({', '.join(args[0])});'''
        if name and args:
            try:
                self.__cur.execute(table)
                self.__con.commit()

                # print(f'Table({name}) create successfully!')
            except Error as e:
                print(e)
        else:
            print('Not arguments!')

    def _get_headers(self, table_name: str) -> list:
        headers = []
        info = []
        try:
            info = self.__cur.execute(f'PRAGMA table_info({table_name})').fetchall()
        except Error as e:
            print('_get_headers: ', e)
        for name_column in info: headers.append(name_column[1])

        return headers

    def insert_into(self, name: str, values: tuple):
        headers = self._get_headers(name)
        if 'id' in headers[0]:
            try:
                self.__cur.execute(
                    f'''INSERT OR IGNORE INTO {name} VALUES (NULL, {(", ".join(['?'] * (len(headers) - 1)))});''',
                    values)
            except Error as e:
                print(e)

        else:
            try:
                self.__cur.execute(f'''INSERT OR IGNORE INTO {name} VALUES ({(", ".join(['?'] * len(headers)))});''',
                                   values)
            except Error as e:
                print(e)
        print(f'{Fore.GREEN}database({db}): add mentor successfully!{Fore.RESET}')
        self.__con.commit()

    def select_all_mentors(self) -> list[dict[Any, Any]]:
        select = []
        mentors = []
        headers = self._get_headers('mentors')
        try:
            self.__cur.execute(f"SELECT * FROM mentors;")
            select = self.__cur.fetchall()
        except Error as e:
            print(e)

        for user in select: mentors.append(dict(zip(headers, user)))

        return mentors

    def select_one_mentor(self, user_id) -> dict[Any, Any]:
        mentor = {}
        select = []
        headers = self._get_headers('mentors')
        try:
            self.__cur.execute(f"SELECT * FROM mentors WHERE telegram_id = {user_id};")
            select = self.__cur.fetchall()
        except Error as e:
            print('select_one_mentor:', e)
        if select and headers: mentor = dict(zip(headers, select[0]))

        return mentor

    def update_month(self, user_id, month: int):
        try:
            self.__cur.execute(f'''UPDATE mentors SET month={month} WHERE telegram_id={user_id};''')
        except Error as e:
            print('update_month:', e)

        self.__con.commit()

    def update_in_chart(self, user_id, in_chart: bool):
        try:
            self.__cur.execute(f'''UPDATE mentors SET in_chart={in_chart} WHERE telegram_id={user_id};''')
        except Error as e:
            print('update_month:', e)
        try:
            self.insert_into('mentors_rating', (
                0, 0, 0, 0, user_id))
        except Error as e: print('insert_into(mentors_rating)', e)

        self.__con.commit()

    def select_mentors_for(self, month: int) -> list[dict[Any, Any]]:
        result = []
        mentors = []
        headers = ['telegram_id', 'username', 'first_name', 'in_chart']
        try:
            self.__cur.execute(f"""SELECT telegram_id, username, first_name, in_chart 
            FROM mentors WHERE in_chart=1 AND month>{month};""")
            result = self.__cur.fetchall()
        except Error as e: print('select_mentors_for', e)

        if result:
            for mentor in result: mentors.append(dict(zip(headers, mentor)))
        return mentors

    def select_rating_mentor_for(self, user_id: int) -> dict[Any, Any]:
        headers = ['request', 'wins', 'failure', 'telegram_id']
        result = []
        try:
            self.__cur.execute(f'''SELECT mentors_rating.request,
                                          mentors_rating.wins, 
                                          mentors_rating.failure, 
                                          mentors_rating.mentor_id
    FROM mentors_rating JOIN mentors ON mentors_rating.mentor_id = mentors.id WHERE mentors.telegram_id={user_id}''')

            result = self.__cur.fetchall()
        except Error as e:
            print('select_rating_mentors', e)
        print(result)
        return dict(zip(headers, result)) if result else {}

    def select_rating_all_mentors(self) -> list[dict[Any, Any]]:
        headers = ['request', 'wins', 'failure', 'telegram_id', 'month', 'username', 'first_name']
        result = []
        win_list = []
        try:
            self.__cur.execute(f'''SELECT mentors_rating.request,
                                mentors_rating.wins,
                                mentors_rating.failure, 
                                mentors_rating.mentor_id,
                                mentors.month,
                                mentors.username, 
                                mentors.first_name 
                                FROM mentors_rating JOIN mentors 
                                ON mentors_rating.mentor_id = mentors.telegram_id WHERE mentors.in_chart=1;''')
            result = self.__cur.fetchall()
        except Error as e: print('select_all_rating_mentors:', e)
        if result:
            for member in result: win_list.append(dict(zip(headers, member)))

        return win_list if win_list else []

    def update_reqeust(self):
        result = []
        try:
            self.__cur.execute(f'''SELECT request FROM mentors_rating;''')
            result = self.__cur.fetchone()
        except Error as e: print('select_request:', e)
        if result:
            request = result[0]
            try:
                self.__cur.execute(f'''UPDATE mentors_rating SET request={request + 1};''')
            except Error as e: print('update_request:', e)

        self.__con.commit()

    def update_wins(self, user_id: int):
        headers = ['mentor_id', 'wins']
        result = []
        try:
            self.__cur.execute(f'''SELECT mentor_id, wins FROM mentors_rating WHERE mentor_id = {user_id};''')
            result = self.__cur.fetchone()
        except Error as e: print('select_wins:', e)
        if result:
            mentor = dict(zip(headers, result))
            try:
                self.__cur.execute(f'''UPDATE mentors_rating SET wins={mentor['wins'] + 1} 
                    WHERE mentor_id={mentor['mentor_id']};''')
            except Error as e: print('update_wins:', e)

        self.__con.commit()

    def update_failure(self, user_id: int):
        headers = ['mentor_id', 'failure']
        result = []
        try:
            self.__cur.execute(f'''SELECT mentor_id, failure FROM mentors_rating WHERE mentor_id = {user_id};''')
            result = self.__cur.fetchone()
        except Error as e:
            print('select_failure:', e)
        if result:
            mentor = dict(zip(headers, result))
            try:
                self.__cur.execute(f'''UPDATE mentors_rating SET failure={mentor['failure'] + 1} 
                           WHERE mentor_id={mentor['mentor_id']};''')
            except Error as e:
                print('update_failure:', e)

        self.__con.commit()
