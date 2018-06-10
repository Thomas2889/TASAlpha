import sqlite3, time, datetime, random

conn = sqlite3.connect('test1.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, dateStamp TEXT, keyword TEXT, value REAL)')


def data_entry():
    c.execute("INSERT INTO stuffToPlot VALUES(1450284583, '2018-04-15', 'Python', 5)")
    conn.commit()
    c.close()
    conn.close()


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0, 10)
    c.execute("INSERT INTO stuffToPlot (unix, dateStamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()
    return date + " - " + str(value)


def read_all_from_db():
    c.execute('SELECT * FROM stuffToPlot')
    for row in c.fetchall():
        print(row)


def read_from_db():
    c.execute("SELECT * FROM stuffToPlot WHERE value = 7 AND keyword='Python'")
    [print(row) for row in c.fetchall()]


read_from_db()
'''
for i in range(10):
    print(dynamic_data_entry())
    time.sleep(1)
'''
c.close()
conn.close()
