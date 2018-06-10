import sqlite3, random, threading, time

conn = sqlite3.connect('DataBase.db')
c = conn.cursor()

nextInstance = 0


def add_record(Item, Loc, Respawn=False):

    global nextInstance

    if Item == 1:
        data = "'Milkable:1'"
    elif Item == 2:
        data = "'Mineral:Jasper'"
    elif Item == 3:
        rand = random.randrange(0, 2)
        if rand == 0:
            data = "'Contains:Water'"
        elif rand == 1:
            data = "'Contains:None'"

    if Respawn:
        Respawn = 1
    else:
        Respawn = 0
    while True:
        try:
            c.execute("INSERT INTO Class1 VALUES({}, {}, {}, {}, {})".format(nextInstance, Item, Loc, data, Respawn))
            print('Created:', Item, 'with the InstanceID of:', nextInstance)
            conn.commit()
            break

        except sqlite3.IntegrityError:
            print('Non-Unique InstanceID')


def clean_instances():

    global nextInstance

    while True:

        # Class1

        conn = sqlite3.connect('DataBase.db')
        c = conn.cursor()

        c.execute('SELECT Instance_ID FROM Class1')
        data = c.fetchall()

        foundGap = False
        temp = 0

        for i, val in enumerate(data):
            temp += 1
            if val[0] != i:
                nextInstance = i
                foundGap = True
                break

        if not foundGap:
            nextInstance = temp

        c.close()
        conn.close()

        # End of Class1


class GetCoords:

    @staticmethod
    def x(location):
        loc, _, _, _ = location.split('_')
        loc.replace('\'', '')
        return loc

    @staticmethod
    def y(location):
        _, loc, _, _ = location.split('_')
        loc.replace('\'', '')
        return loc

    @staticmethod
    def z(location):
        _, _, loc, _ = location.split('_')
        loc.replace('\'', '')
        return loc

    @staticmethod
    def d(location):
        _, _, _, loc = location.split('_')
        loc.replace('\'', '')
        return loc


def get_data(data):

    dataDictionary = {}

    dataPairs = data.split(', ')

    for pair in dataPairs:
        a, b = pair.split(':')
        dataDictionary[a] = b

    return dataDictionary


class ReadData:

    @staticmethod
    def class1(search=False, value=False, column=False):
        if search:
            if column:
                c.execute("SELECT {} FROM Class1 WHERE {}={}".format(column, search, value))
                returnVal = c.fetchall()
                return returnVal

            else:
                c.execute("SELECT * FROM Class1 WHERE {}={}".format(search, value))
                returnVal = c.fetchall()
                return returnVal

        else:
            if column:
                c.execute("SELECT {} FROM Class1".format(column))
                returnVal = c.fetchall()
                return returnVal

            else:
                c.execute("SELECT * FROM Class1")
                returnVal = c.fetchall()
                return returnVal

    @staticmethod
    def object_id_list(id=False):

        if not id:
            c.execute('SELECT * FROM ObjectIdList')

            for row in c.fetchall():
                print(str(row[0]))
        else:
            c.execute('SELECT * FROM ObjectIdList WHERE Object_ID = ?', (id))


# Instance_ID Cleaning Daemon
InstanceCleanerDaemon = threading.Thread(target=clean_instances, args=())
InstanceCleanerDaemon.daemon = True
InstanceCleanerDaemon.start()

for row in ReadData.class1('Object_ID', "3"):
    print(row)
