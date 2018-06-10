import sqlite3, random, threading, time

# conn = sqlite3.connect('Database.db')
# c = conn.cursor()

Player_Location = "'0_0_0_0'"


class Database:

    def find_ai(self, loc):

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        c.execute("SELECT Instance_ID FROM Objects WHERE Location={}".format(loc))
        fetchData = c.fetchall()

        c.close()
        conn.close()

        return fetchData


class GameUpdate:

    @staticmethod
    def ai_updates(args):

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        print("Updating {}'s location to {}".format(args['AI_ID'], args['AI_DEST']))

        c.execute("UPDATE Objects SET Location = {} WHERE Instance_ID = {}".format
                  ('\'' + str(args['AI_DEST'] + '\''), args['AI_ID']))

        conn.commit()

        c.close()
        conn.close()

    def step(self, args):

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        for i in args:
            if i == 'AI_ID':
                self.ai_updates(args)
                break

        c.close()
        conn.close()


class AI:

    def step(self, ID, locX, locY, locZ, locD):

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        dX = locX
        dY = locY
        dZ = locZ
        dD = locD

        if locX < 0:
            dX += 1
        elif locX > 0:
            dX -= 1

        elif locY < 0:
            dY += 1
        elif locY > 0:
            dY -= 1

        elif locZ < 0:
            dZ += 1
        elif locZ > 0:
            dZ -= 1

        c.close()
        conn.close()

        destination = str(dX) + '_' + str(dY) + '_' + str(dZ) + '_' + str(dD)

        args = {'AI_ID': ID, 'AI_DEST': destination}

        loc = str(locX) + '_' + str(locY) + '_' + str(locZ) + '_' + str(locD)

        if destination != loc:
            GameUpdate.step(GameUpdate, args)


def search_area(origin):

    conn = sqlite3.connect('Database.db')
    c = conn.cursor()

    searchRadius = 3

    while True:

        print('##################################################################')

        origin = origin.replace('\'', '')
        X, Y, Z, D = origin.split('_')

        maxX = int(X) + searchRadius
        maxY = int(Y) + searchRadius
        maxZ = int(Z) + searchRadius

        minX = int(X) - searchRadius
        minY = int(Y) - searchRadius
        minZ = int(Z) - searchRadius

        print('Max:', str(maxX), str(maxY), str(maxZ), '   Origin:', str(X), str(Y), str(Z), '   Min:', str(minX),
              str(minY), str(minZ), '   Dimension:', str(D))

        for iX in range(minX, maxX+1):
            for iY in range(minY, maxY+1):
                for iZ in range(minZ, maxZ+1):
                    for ID in Database.find_ai(Database, "'{}_{}_{}_{}'".format(iX, iY, iZ, D)):
                        for i in ID:
                            AI.step(AI, i, iX, iY, iZ, D)


AIcontroller = threading.Thread(target=search_area, args=(Player_Location,))
AIcontroller.daemon = True
AIcontroller.start()

"""
next_instance = 0

for iX in range(-3, 4):
    for iY in range(-3, 4):
        for iZ in range(-3, 4):
            Loc = str(iX) + '_' + str(iY) + '_' + str(iZ) + '_' + str(0)
            c.execute("INSERT INTO Objects VALUES({}, {}, '{}', {}, {})".format(next_instance, 1, Loc, 'Null', 0))
            next_instance += 1

conn.commit()
"""

time.sleep(999999)
