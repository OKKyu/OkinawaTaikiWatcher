#! python3
# -*- coding:utf-8 -*-
import sqlite3
import traceback
from pathlib import Path

dbname = "../db/okinawa-taiki.sqlite3"
dbname2 = "../db/admin.sqlite3"


def create_t_taiki(dbname):
    ret_cd = 0

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " CREATE TABLE T_TAIKI ( "
        sql += "  kyoku      text default '' not null, "
        sql += "  date       text default '' not null, "
        sql += "  hour       integer default 0 not null, "
        sql += "  substitute text default 0 not null, "
        sql += "  value      float default 0 not null, "
        sql += "  criteria   float default 0 not null, "
        sql += "  alerted_flg  integer default 0 not null, "
        sql += "  PRIMARY KEY (kyoku, date, hour, substitute) "
        sql += ")"
        c.execute(sql)
        '''
          alerted_flg : if that record has already announced, set 1, else set 0. (boolean value)
        '''

    except Exception as ex:
        ret_cd = 1
        print(ex)
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

        return ret_cd


def insert_t_taiki(dbname, data):
    ret_cd = 0

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " INSERT INTO T_TAIKI VALUES (?, ?, ?, ?, ?, ?, 0)"
        c.execute(sql, data)

        conn.commit()

    except sqlite3.Error as sqerr:
        print("Exception class is: ", sqerr.__class__)
        print('SQLite error: {}'.format(' '.join(sqerr.args)))

        if sqerr.args[0].split(":")[0] == 'UNIQUE constraint failed':
            ret_cd = 2
        else:
            ret_cd = 1

        print(ex)
        if c is not None:
            conn.rollback()

    except Exception as ex:
        ret_cd = 1
        print(ex)
        if c is not None:
            conn.rollback()

    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

        return ret_cd


def update_t_taiki(dbname, data):
    ret_cd = 0

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        # sorting data
        data = data[4:6] + data[0:4]

        sql = " UPDATE T_TAIKI SET value = ?, criteria = ? WHERE"
        sql += " kyoku = ? and"
        sql += " date = ? and"
        sql += " hour = ? and"
        sql += " substitute = ?"
        c.execute(sql, data)

        conn.commit()

    except Exception as ex:
        ret_cd = 1
        print(ex)
        if c is not None:
            conn.rollback()
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

        return ret_cd


def update_t_taiki_alerted(dbname, data):
    ret_cd = 0

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        # sorting data
        data = data[4:5] + data[0:4]

        sql = " UPDATE T_TAIKI SET alerted_flg = ? WHERE"
        sql += " kyoku = ? and"
        sql += " date = ? and"
        sql += " hour = ? and"
        sql += " substitute = ?"
        c.execute(sql, data)

        conn.commit()

    except Exception as ex:
        ret_cd = 1
        print(ex)
        if c is not None:
            conn.rollback()
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

        return ret_cd


def delete_t_taiki(dbname, data):
    ret_cd = 0
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " DELETE  FROM T_TAIKI WHERE "
        sql += " kyoku = ? and"
        sql += " date = ? and"
        sql += " hour = ? and"
        sql += " substitute = ?"
        c.execute(sql, data)
        conn.commit()

    except Exception as ex:
        ret_cd = 1
        print(ex)
        if c is not None:
            conn.rollback()
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

        return ret_cd


def select_t_taiki(dbname, data):

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " SELECT *  FROM T_TAIKI WHERE "
        sql += " kyoku = ? and"
        sql += " date = ? and"
        sql += " hour = ? and"
        sql += " substitute = ?"
        c.execute(sql, data)

        return c.fetchone()

    except Exception as ex:
        print(ex)
        return None
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def select_t_taiki_justbefore(dbname, data):

    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " SELECT *  FROM T_TAIKI WHERE "
        sql += " kyoku = ? and "
        sql += " substitute = ? "
        sql += "ORDER BY date desc, hour desc "
        sql += "LIMIT 2 "
        c.execute(sql, data)

        d = None

        for item in c.fetchall():
            d = item

        return d

    except Exception as ex:
        print(ex)
        return None
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def select_t_criterias_all(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " SELECT substitute, criteria  FROM webfront_criterias "
        c.execute(sql)

        d = {}

        for name, value in c.fetchall():
            d.setdefault(name, value)

        return d

    except Exception as ex:
        print(ex)
        return None
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def select_t_kyokus_all(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " SELECT * FROM webfront_kyokus "
        c.execute(sql)

        d = {}

        for item in c.fetchall():
            d.setdefault(item[1], item)

        return d

    except Exception as ex:
        print(ex)
        return None
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def select_t_settings(dbname):
    '''
       boolean value{1:true 0:false}
    '''
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        sql = " SELECT * FROM webfront_settings "
        c.execute(sql)

        return c.fetchall()[0]

    except Exception as ex:
        print(ex)
        return None
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    # create_t_taiki(dbname)

    #insert_t_taiki(dbname, ("那覇", "20230904", 11, "SO2", 0.44, 0.31))
    #print(select_t_taiki(dbname, ("那覇", "20230904", 11, "SO2")))

    #update_t_taiki(dbname, (0.21, 0.55, "那覇", "20230904", 11, "SO2"))
    #print(select_t_taiki(dbname, ("那覇", "20230904", 11, "SO2")))

    #delete_t_taiki(dbname, ("那覇", "20230904", 11, "SO2"))
    #print(select_t_taiki(dbname, ("那覇", "20230904", 11, "SO2")))

    #result = select_t_settings(dbname2)
    # print(result)

    #result = select_t_taiki_justbefore(dbname, ("名護", "NO"))
    result = select_t_kyokus_all(dbname2)
    print(result)
