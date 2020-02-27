import json, time
import uuid
from .sql import sql
from .elastic import es
import requests
import hashlib


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
                (id_to  , id_point, date, None))
            else:
                return [False, "Invalid right", 403]
            if not succes:
                return [False, "data input error", 500]
        return [True, {}, None]

    def infos(self,
              id_points = None,
              period_start = None,
              period_end = None,
              longlat = None,
              range = None):
        if period_end and period_start:
            if period_start > period_end:
                return [False, "'period_start' should be before 'period_end'", 400]
        prop = self.__get_point("proprietary")
        shar = self.__get_point("shared")
        if id_points:
            prop = list(set(prop).intersection(id_points))
            shar = list(set(shar).intersection(id_points))
        prop = es.search(body=self.__infos_query(prop, [], period_start, period_end))
        shar = es.search(body=self.__infos_query(shar, [], period_start, period_end))
        return [True, {"points": {"proprietary": prop, "shared": shar }}, None]

    def adddata(self, data, id_sig, id_point):
        id_sig = __hash(id_sig)
        id_point = __hash(id_point)
        date = int(round(time.time() * 1000))
        input={
            "id_sig": id_sig,
            "id_point": id_point,
            "data": data,
            "date": date
        }
        res = es.index(index='point_test',body=input)
        return [True, {"data_added": input}, None]

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

    def __get_point(self, type = "proprietary"):
        res = []
        if type == "proprietary":
            res = sql.get("SELECT id FROM `point` WHERE id_user = %s", (self.usr_id))
        elif type == "shared":
            res = sql.get("SELECT id FROM `point_shared` WHERE id_user = %s", (self.usr_id))
        ret = []
        for i in res:
            ret.append(i[0])
        return ret

    def __infos_query(self, id_points, id_sigs, date_start = None, date_end = None):
        query = {
            	"sort": [ {"date": "desc"} ],
            	"query": {"bool":{"must":[
                            {"range":{"date":{}}},
            				{"term":{ "_index":"point_test"}},
            				{"bool":{ "should":[]}}
            	 ]}}}
        for id in id_points:
            query["query"]["bool"]["must"][2]["bool"]["should"].append(
                {"term":{"id_point": self.__hash(id)}}
            )
        for id in id_sigs:
            query["query"]["bool"]["must"][2]["bool"]["should"].append(
                {"term":{"id_sig": self.__hash(id)}}
            )
        if date_start:
            query["query"]["bool"]["must"][0]["range"]["date"]["gte"] = date_start
        if date_end:
            query["query"]["bool"]["must"][0]["range"]["date"]["gte"] = date_end
        return query

    def __hash(self, string):
        return  None if not string else hashlib.sha256(str(string).encode('utf-8')).hexdigest()
