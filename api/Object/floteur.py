import json
import uuid
import time
from .sql import sql

class floteur:
    def __init__(self, usr_id = -1):
        self.usr_id = str(usr_id)

    def add(self, id_sig):
        number = sql.get("SELECT COUNT(*) FROM `point` WHERE id_user = %s", (self.usr_id))[0][0]
        name = "point_" + str(number)
        succes = sql.input("INSERT INTO `point` (`id`, `id_user`, `id_sig`, `name`, `surname`) VALUES (NULL, %s, %s, %s, %s)", \
        (int(self.usr_id), id_sig, name, name))
        if not succes:
            return [False, "data input error", 500]
        return [True, {}, None]

    def delete(self, id_points):
        return

    def rename(self, id_point, surname):
        if not self.__exist(id_point):
            return [False, "Invalid point_id", 400]
        succes = False
        if self.__proprietary(id_point):
            succes = sql.input("UPDATE `point` SET surname = %s WHERE id = %s AND id_user = %s", (surname, id_point, self.usr_id))
        elif self.__shared(id_point):
            succes = sql.input("UPDATE `point_shared` SET surname = %s WHERE id_point = %s AND id_user = %s", (surname, id_point, self.usr_id))
        else:
            return [False, "Invalid right", 403]
        if not succes:
            return [False, "data input error", 500]
        return [True, {}, None]

    def share(self, id_points, email):
        if not isinstance(id_points, list):
            return [False, "Id_points should be a list", 400]
        for id_point in id_points:
            if not self.__exist(id_point):
                return [False, "Invalid point_id", 400]
            succes = False
            if self.__proprietary(id_point):
                id_to = sql.get("SELECT id FROM `user` WHERE email = %s", (email))
                if len(id_to) < 1:
                    return [False, "Invalid email", 400]
                id_to = id_to[0]
                if id_to != self.usr_id:
                    return [False, "Can't share to yourself", 401]
                date = str(int(round(time.time() * 1000)))
                succes =  sql.input("INSERT INTO `point_shared` (`id`, `id_user`, `id_point`, `date`, `surname`) VALUES (NULL, %s, %s, %s, %s)", \
                (id_to, id_point, date, None))
            else:
                return [False, "Invalid right", 403]
            if not succes:
                return [False, "data input error", 500]
        return [True, {}, None]

    def infos(self,
              longlat = None,
              range = None,
              id_points = None,
              period_start = None,
              period_end = None):

        return

    def adddata(self, data, id_sig = None, id_point = None):

        return

    def __exist(self, id_point):
        ret = False
        if sql.get("SELECT COUNT(*) FROM `point` WHERE id = %s", (id_point))[0][0] > 0:
            ret = True
        return ret

    def __proprietary(self, id_point):
        ret = False
        if sql.get("SELECT COUNT(*) FROM `point` WHERE id_user = %s AND id = %s", (self.usr_id, id_point))[0][0] > 0:
            ret = True
        return ret

    def __shared(self, id_point):
        ret = False
        if sql.get("SELECT COUNT(*) FROM `point_shared` WHERE id_user = %s AND id_point = %s", (self.usr_id, id_point))[0][0] > 0:
            ret = True
        return ret
