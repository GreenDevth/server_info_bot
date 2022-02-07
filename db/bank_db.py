from db.players_db import *


def bank_balance(discord_id):
    res = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        check = player_exists(discord_id)
        if check == 1:
            sql = 'SELECT * FROM scum_players WHERE DISCORD_ID=%s'
            cur.execute(sql, (discord_id,))
            row = cur.fetchone()
            while row is not None:
                res = list(row)
                return res
        if check == 0:
            return res
        return res
    except Error as e:
        print(e)


def player_coins(discord_id):
    try:
        check = player_exists(discord_id)
        if check == 1:
            conn = MySQLConnection(**db)
            cur = conn.cursor()
            sql = 'SELECT COINS FROM scum_players WHERE DISCORD_ID = %s'
            cur.execute(sql, (discord_id,))
            row = cur.fetchone()
            while row is not None:
                res = list(row)
                return int(res[0])
        else:
            pass

    except Error as e:
        print(e)


def player_bank_id(discord_id):
    try:
        check = player_exists(discord_id)
        if check == 1:
            conn = MySQLConnection(**db)
            cur = conn.cursor()
            sql = 'SELECT BANK_ID FROM scum_players WHERE DISCORD_ID = %s'
            cur.execute(sql, (discord_id,))
            row = cur.fetchone()
            while row is not None:
                res = list(row)
                return res[0]
        else:
            pass
    except Error as e:
        print(e)


def player_discord_id(bank_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT DISCORD_ID FROM scum_players WHERE BANK_ID = %s'
        cur.execute(sql, (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def player_coins_bank(bank_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COINS FROM scum_players WHERE BANK_ID = %s'
        cur.execute(sql, (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def transfer_coin(owner_id, amount, another_bank_id):
    check = player_exists(owner_id)
    if check == 1:
        owner_coin = player_coins(owner_id)  # Get current coins from discord id.
        coins = int(amount)  # Convert str to int
        another_id = player_discord_id(another_bank_id)

        if owner_coin < coins:
            msg = "ขออภัยทำรายการไม่สำเร็จ เนื่องจากยอดเงินของคุณไม่เพียงพอ"
            return msg.strip()
        else:
            transfer = minus_coins(owner_id, coins)
            plus_coins(another_id, coins)
            return transfer


def minus_coins(discord_id, coins):
    """ minus coins from players """
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        current_coin = player_coins(discord_id)
        minus = current_coin - coins
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (minus, discord_id,))
        conn.commit()
        total = player_coins(discord_id)
        msg = 'ทำรายการสำเร็จ ยอดเงินคงเหลือ ${:,d}'.format(total)
        return msg.strip()
    except Exception as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def minus_coins_store(discord_id, coins):
    """ minus coins from players """
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        current_coin = player_coins(discord_id)
        if current_coin < coins:
            return 0
        if coins < current_coin:
            minus = current_coin - coins
            sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
            cur.execute(sql, (minus, discord_id,))
            conn.commit()
            return 1
    except Exception as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def plus_coins(discord_id, coins):
    """ Plus Coin to player """
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        current_coin = player_coins(discord_id)
        plus = current_coin + coins
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (plus, discord_id))
        conn.commit()
        total = player_coins(discord_id)
        msg = 'ทำรายการสำเร็จ ยอดเงินของคุณตอนนี้คือ **${:,d}**'.format(total)
        return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def get_coin_from_bank(bank_id):
    """ Get Information bank from scum player by bank id """

    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COINS , DISCORD_ID FROM scum_players WHERE BANK_ID = %s'
        cur.execute(sql, (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res

    except Error as e:
        print(e)


def get_package_price(package_name):
    """ Get Package Price for scum package db """

    try:

        """ Get Price from package name """
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT package_price FROM scum_package WHERE package_name = %s'
        cur.execute(sql, (package_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        cur.close()

    except Error as e:
        print(e)


def get_player_bank(dicord_id):
    """ Get Players Bank_id """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT BANK_ID FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (dicord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_bank_id(discord_id):
    """ Get Bank id for discord id """

    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT BANK_ID FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def add_coins(amount, discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        check = get_bank_id(discord_id)
        if check is not None:
            coins = get_coin_from_bank(check)
            coins = list(coins)
            player_coin = coins[0]
            total = int(player_coin) + int(amount)
            sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
            cur.execute(sql, (total, discord_id,))
            conn.commit()
            msg = f'ระบบได้เติมเงินให้กับ Bank ID หมายเลข `` {check} `` จากจำนวน `` {player_coin} `` เป็นจำนวน `` {total} `` เรียบร้อย'
            return msg.strip()
        if check is None:
            msg = "ทำรายการไม่สำเร็จ ไม่พบข้อมูลผู้รับเงิน"
            return msg.strip()

    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def remove_coins(amount, discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        check = get_bank_id(discord_id)
        if check is not None:
            coins = get_coin_from_bank(check)
            coins = list(coins)
            player_coin = coins[0]
            total = int(player_coin) - int(amount)
            sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
            cur.execute(sql, (total, discord_id,))
            conn.commit()
            msg = f'ระบบได้หักเงินจาก Bank ID หมายเลข `` {check} `` จากจำนวน `` {player_coin} `` คงเหลือจำนวน `` {total} `` เรียบร้อย'
            return msg.strip()
        if check is None:
            msg = "ทำรายการไม่สำเร็จ ไม่พบข้อมูลผู้รับเงิน"
            return msg.strip()

    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

