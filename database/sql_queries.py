mentors_headers = (
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'is_admin BOOL',
    'telegram_id INTEGER',
    'first_name STRING',
    'second_name STRING',
    'username STRING',
    'in_chart BOOL DEFAULT 0',
    'month INTEGER DEFAULT 1, '
    'UNIQUE (telegram_id)')

mentors_rating_headers = (
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'request INTEGER',
    'wins INTEGER',
    'failure INTEGER',
    'rating REAL',
    'mentor_id INTEGER, '
    'FOREIGN KEY (mentor_id) REFERENCES mentors(telegram_id)')
