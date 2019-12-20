import pymysql

class sql:
    def get(query, data):
        db = pymysql.connect("datab","wellcheck","1q2W3e4R","wellcheck" )
        cursor = db.cursor()
        cursor.execute(query, data)
        to_ret =  cursor.fetchall()
        cursor.close()
        db.close()
        return to_ret

    def input(query, data):
        db = pymysql.connect("datab","wellcheck","1q2W3e4R","wellcheck" )
        cursor = db.cursor()
        try:
            cursor.execute(query, data)
            db.commit()
            to_ret = True
        except:
            db.rollback()
            to_ret = False
        cursor.close()
        db.close()
        return to_ret
