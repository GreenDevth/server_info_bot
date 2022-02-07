from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def player_steam(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT STEAM_ID FROM scum_players WHERE DISCORD_ID=%s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def player_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COUNT(*) FROM scum_players WHERE DISCORD_ID=%s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def new_scum_players(discord_name, discord_id, steam_id, bank_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_players(DISCORD_NAME, DISCORD_ID, STEAM_ID, BANK_ID) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (discord_name, discord_id, steam_id, bank_id))
        conn.commit()
        return 1
    except Error as e:
        print(e)
        return 0
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def remove_players(discord_id):
    conn = None
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cur = conn.cursor()
        cur.execute('SELECT steam_id FROM scum_players WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            data = list(row)
            steam_id = data[0]
            cur.execute('DELETE FROM scum_players WHERE discord_id = %s', (discord_id,))
            conn.commit()
            cur.close()
            msg = "ระบบได้ทำการลบข้อมูล สตรีมหมายเลข {} เป็นที่เรียบร้อยแล้ว".format(steam_id)
            return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

