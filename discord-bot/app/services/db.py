from uuid import uuid4

import sqlite3 as sql
import os


class DbEngine:
    """
    Log Functions
    """
    def save_log(self, log_entry: dict) -> None:
        db_file = self.check_exists()

        log_id = str(uuid4())
        log_date = log_entry["date"]
        log_time = log_entry["time"]
        log_user_id = log_entry["user_id"]
        log_action = log_entry["action"]
        log_reason = log_entry["reason"]
        log_details = log_entry["details"]

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            srch = 'INSERT INTO logs(id, date, time, user_id, action, reason, details) VALUES (?,?,?,?,?,?,?)'
            vals = (log_id, log_date, log_time, log_user_id, log_action, log_reason, log_details)

            try:
                cur.execute(srch, vals)
            
            except sql.Error as sql_error:
                raise sql_error
            
            except Exception as e:
                raise e
            
    """
    Suggestion Functions
    """            
    def save_suggestion(self, suggestion: dict) -> None:
        db_file = self.check_exists()

        sugg_id = str(uuid4())
        sugg_date = suggestion["date"]
        sugg_time = suggestion["time"]
        sugg_user_id = suggestion["user_id"]
        sugg_user_jdate = suggestion["join_date"]
        sugg_user_details = suggestion["details"]
        sugg_status = suggestion["status"]

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            srch = 'INSERT INTO suggestions(id, date, time, user_id, join_date, suggestion, status) VALUES (?,?,?,?,?,?,?)'
            vals = (sugg_id, sugg_date, sugg_time, sugg_user_id, sugg_user_jdate, sugg_user_details, sugg_status)

            try:
                cur.execute(srch, vals)
            
            except sql.Error as sql_error:
                raise sql_error
            
            except Exception as e:
                raise e
            
    def get_all_suggestions(self) -> list:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            results = cur.execute('SELECT id, date, time, user_id, join_date, suggestion, status FROM suggestions').fetchall()

            return results
        
    def get_open_suggestions(self) -> list:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            results = cur.execute(
                'SELECT id, date, time, user_id, join_date, suggestion, status FROM suggestions WHERE status=?',
                ("open",)
            ).fetchall()
        
            return results
        
    def get_closed_suggestions(self) -> list:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            results = cur.execute(
                'SELECT id, date, time, user_id, join_date, suggestion, status FROM suggestions WHERE status=?',
                ("closed",)
            ).fetchall()
        
            return results
        
    def close_suggestion(self, _id: str) -> bool:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            try:
                cur.execute(
                    'UPDATE suggestions SET status=? WHERE id=?',
                    ("closed", _id,)
                )
                return True
            except Exception as e:
                print(e)
                raise e
            
    def search_suggestion(self, _id: str) -> bool:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            srch = 'SELECT * FROM suggestions WHERE id=?'
            val = (_id, )

            try:
                cur.execute(srch, val).fetchone()
                return True
            except Exception as e:
                return False

    """
    Restricted Words Functions
    """
    def search_word(self, word: str) -> bool:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            all_words = cur.execute(
                'SELECT word FROM words'
            ).fetchall()

            for existing_word in all_words:
                if word == existing_word[0]:
                    return True
                
        return False

    def save_word(self, word: str):
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            try:
                cur.execute(
                    'INSERT INTO words(id, word) VALUES (?,?)',
                    (str(uuid4()), word)
                )

                return True
            
            except sql.Error:
                return False
            except Exception as e:
                raise e
            
    def remove_word(self, word: str) -> bool:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            try:
                all_words = cur.execute('SELECT word FROM words').fetchall()
                
                for stored_word in all_words:
                    if stored_word[0] == word:
                        try:
                            cur.execute('DELETE FROM words WHERE word=?', (word,))
                            return True
                        except Exception as e:
                            raise e
            except Exception as e:
                raise e
            
    def get_all_words(self):
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            try:
                all_words = cur.execute(
                    'SELECT id, word FROM words'
                ).fetchall()

                return all_words
            except sql.Error:
                return []
            except Exception as e:
                raise e

    """
    Music playlist functions
    """
    def get_playlists(self, user_id: int) -> list:
        db_file = self.check_exists()

        with sql.connect(db_file) as mdb:
            cur = mdb.cursor()

            srch = 'SELECT playlist_name FROM playlists WHERE id=?'
            val = (user_id, )

            try:
                results = cur.execute(srch, val).fetchall()
                return results
            except Exception as e:
                raise e

    """
    Universal Functions
    """
    def check_exists(self):
        curr_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        app_dir = os.path.dirname(curr_dir)
        data_dir = os.path.join(app_dir, "data")

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        return_file = os.path.join(data_dir, "main.db")

        try:
            self.create_tables(return_file)
            return return_file
        except sql.Error as sql_error:
            raise sql_error
        except Exception as e:
            raise e
    
    def create_tables(self, file_name: str) -> None:
        with sql.connect(file_name) as mdb:
            cur = mdb.cursor()

            try:
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS logs(
                        id TEXT NOT NULL PRIMARY KEY,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        action TEXT NOT NULL,
                        reason TEXT NOT NULL,
                        details TEXT,
                        UNIQUE(id)
                    )
                    '''
                )

                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS suggestions(
                        id TEXT NOT NULL PRIMARY KEY,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        join_date TEXT NOT NULL,
                        suggestion TEXT NOT NULL,
                        status TEXT NOT NULL,
                        UNIQUE(id,suggestion)
                    )
                    '''
                )

                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS words(
                        id TEXT NOT NULL PRIMARY KEY,
                        word TEXT NOT NULL,
                        UNIQUE(word)
                    )
                    '''
                )

                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS playlists(
                        id INTEGER NOT NULL PRIMARY KEY,
                        playlist_name TEXT NOT NULL,
                        url TEXT NOT NULL
                    )
                    '''
                )
            except sql.Error as sql_error:
                raise sql_error
            except Exception as e:
                raise e
