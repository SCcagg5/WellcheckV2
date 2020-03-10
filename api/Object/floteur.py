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
        date = str(int(round(time.time() * 1000)))
        succes = sql.input("INSERT INTO `point` (`id`, `id_user`, `id_sig`, `name`, `surname`, `date`) VALUES (NULL, %s, %s, %s, %s, %s)", \
        (int(self.usr_id), id_sig, name, name, date))
        if not succes:
            return [False, "data input error", 500]
        return [True, {}, None]

    def delete(self, id_points):
        return

    def rename(self, id_point, surname):
        if not self.__exist(id_point):
            return [False, "Invalid point_id: '" + id_point + "'", 400]
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
                return [False, "Invalid id_point: id_point : '" + str(id_point) + "'", 400]
            succes = False
            if self.__proprietary(id_point):
                id_to = sql.get("SELECT id FROM `user` WHERE email = %s", (email))
                if len(id_to) < 1:
                    return [False, "Invalid email: '" + email + "'", 400]
                id_to = str(id_to[0][0])
                if id_to == self.usr_id:
                    return [False, "Can't share to yourself: id_point : '" + str(id_point) + "'", 401]
                if self.__shared(id_point, id_to):
                    return [False, "Already shared with: '"+ email +"'", 401]
                date = str(int(round(time.time() * 1000)))
                number = sql.get("SELECT COUNT(*) FROM `point_shared` WHERE id_user = %s", (id_to))[0][0]
                name = "point_" + str(number)
                succes =  sql.input("INSERT INTO `point_shared` (`id`, `id_user`, `id_point`, `date`, `surname`) VALUES (NULL, %s, %s, %s, %s)", \
                (id_to, id_point, date, name))
                if not succes:
                    return [False, "data input error", 500]
            else:
                return [False, "Invalid right : id_point : '" + str(id_point) + "'", 403]
        return [True, {}, None]

    def my_shares(self):
        res = sql.get("SELECT point_shared.id_point, user.email, point_shared.date FROM point_shared INNER JOIN user ON point_shared.id_user = user.id INNER JOIN point ON point_shared.id_point = point.id WHERE point.id_user = %s", (self.usr_id))
        ret = {}
        for i in res:
            index = str(i[0])
            if index not in ret:
                ret[index] = []
            ret[index].append({
                "email": i[1],
                "date": i[2]
            })
        return [True, {"shares": ret} , None]

    def infos_points(self,
              id_points = None,
              period_start = None,
              period_end = None,
              longlat = None,
              range = None,
              limit = None):
        if period_end and period_start:
            if period_start > period_end:
                return [False, "'period_start' should be before 'period_end'", 400]
        prop = self.__get_point("proprietary")
        shar = self.__get_point("shared")
        if id_points:
             prop = list(set(prop).intersection(id_points))
             shar = list(set(shar).intersection(id_points))
        propdetail = self.__get_point("proprietary", details=True)
        shardetail = self.__get_point("shared", details=True)
        propdata = self.__infos_query(prop, period_start, period_end, limit)
        shardata = self.__infos_query(shar, period_start, period_end, limit)
        ret = {
            "proprietary": [],
            "shared": []
        }
        for i in prop:
             propdetail[str(i)]["data"] = propdata[str(i)] if str(i) in propdata else []
             ret["proprietary"].append(propdetail[str(i)])
        for i in shar:
             shardetail[str(i)]["data"] = shardata[str(i)] if str(i) in shardata else []
             ret["shared"].append(shardetail[str(i)])
        return [True, {"points": ret}, None]

    def infos_point(self, id_point, period_start, period_end, limit = 100000000):
        if not self.__exist(id_point):
            return [False, "Invalid id_point: '" + id_point + "'", 400]
        status = "proprietary" if self.__proprietary(id_point) else "shared" if self.__shared(id_point) else None
        if not status:
            return [False, "Invalid right", 403]
        ret = self.__get_point(status, details=True)[str(id_point)]
        res = self.__infos_query([id_point], period_start, period_end, limit)
        ret["data"] = res[str(id_point)] if str(id_point) in res else []
        return [True, ret, None]

    def adddata(self, data, id_sig, id_point):
        id_sig = self.__hash(id_sig)
        id_point = id_point
        date = int(round(time.time() * 1000))
        if "pos" not in data or not data["pos"]:
            return [False, "Missing index 'pos' inside data", 400]
        if "lon" not in data['pos'] or "lat" not in data['pos']:
            return [False, "Missing inbex 'lon' or 'lat' inside data.pos", 400]
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
        try:
            if sql.get("SELECT COUNT(*) FROM `point` WHERE id = %s", (id_point))[0][0] > 0:
                ret = True
        except:
            ret = False
        return ret

    def __proprietary(self, id_point):
        ret = False
        try:
            if sql.get("SELECT COUNT(*) FROM `point` WHERE id_user = %s AND id = %s", (self.usr_id, id_point))[0][0] > 0:
                ret = True
        except:
            ret = False
        return ret

    def __shared(self, id_point, id_user = None):
        ret = False
        try:
            if sql.get("SELECT COUNT(*) FROM `point_shared` WHERE id_user = %s AND id_point = %s", (id_user if id_user else self.usr_id, id_point))[0][0] > 0:
                ret = True
        except:
            ret = False
        return ret

    def __get_point(self, type = "proprietary", details = False):
        res = []
        if type == "proprietary":
            if details:
                res = sql.get("SELECT `id`, `name`, `surname`, `date` FROM `point` WHERE id_user = %s", (self.usr_id))
                ret = {}
                for i in res:
                    ret[str(i[0])] = {
                            "id": i[0],
                            "name": i[1],
                            "surname": i[2],
                            "date": i[3]
                        }
            else:
                res = sql.get("SELECT id FROM `point` WHERE id_user = %s", (self.usr_id))
                ret = []
                for i in res:
                    ret.append(i[0])
        elif type == "shared":
            if details:
                res = sql.get("SELECT point.id, point.name, point_shared.surname, point_shared.date FROM `point_shared` INNER JOIN `point` ON `id_point` = point.id WHERE point_shared.id_user = %s", (self.usr_id))
                ret = {}
                for i in res:
                    ret[str(i[0])] = {
                            "id": i[0],
                            "name": i[1],
                            "surname": i[2],
                            "date": i[3]
                        }
            else:
                res = sql.get("SELECT id FROM `point_shared` WHERE id_user = %s", (self.usr_id))
                ret = []
                for i in res:
                    ret.append(i[0])
        return ret

    def __infos_query(self, id_points, date_start = None, date_end = None, limit = None):
        range = {"from": "0"}
        if date_start:
            range["from"] = str(date_start)
        if date_end:
            range["to"] = str(date_end)
        limit = limit if limit else 5
        query = {
          "size": -1,
          "aggs" : {
            "date_range" : {
              "range" : { "field" : "date", "ranges" : [range]},
              "aggs": {
                "dedup" : {
                  "filter": {"terms": {"id_point": id_points}},
                      "aggs": {
                        "dedup" : {
                          "terms":{"field": "id_point"},
                          "aggs": {
                            "top_sales_hits": {
                              "top_hits": {
                                "sort": [{"date": {"order": "desc"}}],
                                "_source": {"includes": [ "date", "data" ]},
                                "size" : limit
                              }
                            }
                          }
                        }
                      }
                    }
                }
            }
          }
        }
        res = es.search(index="point_test", body=query)
        ret = {}
        for i in res["aggregations"]["date_range"]["buckets"][0]["dedup"]["dedup"]["buckets"]:
            ret[str(i["key"])] = []
            for i2 in i["top_sales_hits"]["hits"]["hits"]:
                if "date" in i2["_source"]:
                    i2["_source"]["date"] = str(i2["_source"]["date"])
                ret[str(i["key"])].append(i2["_source"])
        return ret

    def __hash(self, string):
        return  None if not string else hashlib.sha256(str(string).encode('utf-8')).hexdigest()
