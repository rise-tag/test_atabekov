import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    def search_user_by_name(self, username):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            return cursor.fetchone()
        except Error as e:
            print(f"Ошибка при поиске пользователя: {e}")
            return None

    def execute_transaction(self, operations):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            self.conn.execute('BEGIN TRANSACTION')
            for op in operations:
                op()
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка при выполнении транзакции: {e}")

class User(DatabaseManager):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.open_connection()
        self.create_table()

    def create_table(self):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def add_user(self, username, email):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")

    def get_user_by_id(self, user_id):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Ошибка при получении пользователя по ID: {e}")
            return None

    def delete_user(self, user_id):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

class Admin(User):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.create_admin_table()

    def create_admin_table(self):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    admin_rights TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при создании таблицы администраторов: {e}")

    def add_admin(self, user_id, admin_rights):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO admins (user_id, admin_rights) VALUES (?, ?)", (user_id, admin_rights))
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при добавлении администратора: {e}")

class Customer(User):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.create_customer_table()

    def create_customer_table(self):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    loyalty_points INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при создании таблицы клиентов: {e}")

    def add_customer(self, user_id, loyalty_points):
        if not self.conn:
            print("Соединение с базой данных не установлено.")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO customers (user_id, loyalty_points) VALUES (?, ?)", (user_id, loyalty_points))
            self.conn.commit()
        except Error as e:
            print(f"Ошибка при добавлении клиента: {e}")

if __name__ == "__main__":
    db_file = 'example.db'
    db_manager = DatabaseManager(db_file)
    
    db_manager.open_connection()
    
    user_manager = User(db_file)
    admin_manager = Admin(db_file)
    customer_manager = Customer(db_file)

    user_manager.add_user('sultan', 'sultan@gmail.com')
    user_manager.add_user('baibol', 'baibol@gmail.com')

    sultan_id = user_manager.get_user_by_id(1)[0]
    admin_manager.add_admin(sultan_id, 'full')

    baibol_id = user_manager.get_user_by_id(2)[0]
    customer_manager.add_customer(baibol_id, 100)

    user_data = db_manager.search_user_by_name('sultan')
    print(f"Найденный пользователь: {user_data}")

    def add_user_operations():
        user_manager.add_user('beknazar', 'beknazar@gmail.com')
        user_manager.add_user('beka', 'beka@gmail.com')

    db_manager.execute_transaction([add_user_operations])
    db_manager.close_connection()
