import sqlite3

def get_last_candlestick(symbol):
    conn = sqlite3.connect('candlestick_db.sqlite')
    cursor = conn.cursor()
    query = '''
        SELECT * FROM candlesticks_m1
        WHERE symbol = ?
        ORDER BY timestamp_msec DESC
        LIMIT 1
    '''
    cursor.execute(query, (symbol,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'symbol': result[0],
            'timestamp_msec': result[1],
            'open': result[2],
            'high': result[3],
            'low': result[4],
            'close': result[5],
        }
    return None
