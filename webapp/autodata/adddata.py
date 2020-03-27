import pymysql
import time, sys
from elasticsearch import Elasticsearch
from random import seed
from random import random

seed(1)

es = Elasticsearch(["http://elasticsearch:9200"])

class sql:
    def cred():
        return pymysql.connect("datab", str(sys.argv[1]), str(sys.argv[2]),"wellcheck" )

    def get(query, data):
        db = sql.cred()
        cursor = db.cursor()
        cursor.execute(query, data)
        to_ret =  cursor.fetchall()
        cursor.close()
        db.close()
        return to_ret

    def input(query, data):
        db = sql.cred()
        cursor = db.cursor()
        cursor.execute(query, data)
        db.commit()
        to_ret = True
        cursor.close()
        db.close()
        return to_ret

def upval(num, der, rou, max, min, mod = None):
    if rou != 0:
        f = "{0:."+str(rou)+"f}"
        ret = float(f.format(num - der + (random() * (2 * der))))
    else:
        ret = int(num - der + (random() * (2 * der)))
    if mod:
        i = -rou
        for _ in range(5):
            if mod - 10**i < 0:
                i -= 1
                break
            i += 1
        switch = 10**i
        while _ in range(10):
            if ret % mod == 0:
                break
            ret += switch
    if rou != 0:
        ret = float(f.format(max)) if ret > max else float(f.format(min)) if ret < min else ret
    else:
        ret = int(max) if ret > max else int(min) if ret < min else ret
    return ret

def note(ph, turb, orp, temp):
    ph_point = 1.4*10**-32-29.3*ph+8.19*ph**2-0.56*ph**3
    ph_point = 0 if float(ph_point) < float(0) else 5 if float(ph_point) > float(5) else ph_point
    orp_point = -3.39*10**-32-0.0846*turb+6.73*10**-4*turb**2-1.12*10**-6*turb**3
    orp_point = 0 if float(ph_point) < float(0) else 5 if float(ph_point) > float(5) else ph_point
    temp_point = 5.83+0.235*temp-0.0241*temp**2
    temp_point = 0 if float(orp_point) < float(0) else 6 if float(orp_point) > float(6) else orp_point
    turb_point = 0 if float(turb) < float(921) else 3
    return float("{0:.1f}".format(ph_point + orp_point + temp_point + turb_point))


res =  sql.get("SELECT id FROM `point` WHERE id_sig = -1", ())
points = []
for i in res:
    points.append(i[0])
query = {
  "size": -1,
  "aggs" : {
    "date_range" : {
      "range" : { "field" : "date", "ranges" : {"from": "0"}},
      "aggs": {
        "dedup" : {
          "filter": {"terms": {"id_point": points}},
              "aggs": {
                "dedup" : {
                  "terms":{"field": "id_point"},
                  "aggs": {
                    "top_sales_hits": {
                      "top_hits": {
                        "sort": [{"date": {"order": "desc"}}],
                        "_source": {"includes": [ "date", "data", "id_sig" ]},
                        "size" : 1
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
es.indices.refresh(index="point_test")
res = es.search(index="point_test", body=query)
ret = {}
for i in res["aggregations"]["date_range"]["buckets"][0]["dedup"]["dedup"]["buckets"]:
    ret[str(i["key"])] = []
    for i2 in i["top_sales_hits"]["hits"]["hits"]:
        if "date" in i2["_source"]:
            i2["_source"]["date"] = str(i2["_source"]["date"])
        if "id_sig" in i2["_source"]:
            i2["_source"]["id_sig"] = str(i2["_source"]["id_sig"])
        ret[str(i["key"])].append(i2["_source"])
for i in points:
    data = ret[str(i)][0]['data']['data']
    ph = data["ph"] if "ph" in data else 7
    ph = upval(ph, 0.2, 1, 12.8, 0)
    turbidity = data["turbidity"] if "turbidity" in data else 1000
    turbidity = upval(turbidity, 4, 0, 1024, 0, 5)
    orp = data["turbidity"] if "turbidity" in data else 300
    orp = upval(orp, 2, 1, 400, 220)
    temp = data["temp"] if "temp" in data else 5
    temp = upval(temp, 0.1, 1, 25, 1)
    input={
        "id_sig": ret[str(i)][0]['id_sig'],
        "id_point": i,
        'data': {
           'data': {
               "ph": ph,
               "turbidity": turbidity,
               "orp": orp,
               "temp": temp,
               "note": note(ph, turbidity, orp, temp)
           },
           'pos': {
               'lon': ret[str(i)][0]['data']['pos']['lon'],
               'lat': ret[str(i)][0]['data']['pos']['lat'],
               }
           },
        "date": int(round(time.time() * 1000))
    }
    es.index(index='point_test',body=input)
