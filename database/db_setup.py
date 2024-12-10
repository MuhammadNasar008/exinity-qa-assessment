import sqlite3

def initialize_database():
    conn = sqlite3.connect('candlestick_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candlesticks_m1 (
            symbol TEXT NOT NULL,
            timestamp_msec INTEGER NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            PRIMARY KEY (symbol, timestamp_msec)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
