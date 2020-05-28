import json, datetime, time
import jwt
import hashlib
import time
import os, sys
from .sql import sql
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

class action:
    def __init__(self, userId = -1, filename = None):
        self.userId = str(userId)
        self.filename = filename

    def create(self, company, name):
        id = self.userId
        secret = self.__getsecret()
        time = datetime.datetime.utcnow()
        ret = jwt.encode({'time': str(time), 'id': id, 'password': hash(str(id) + str(secret) + str(time))}, secret).decode('utf-8')
        self.filename = 'ACTION_' + name.replace(' ', '_') + '.pdf' if self.filename is None else self.filename
        documentTitle = 'actions Rocket Bond Sarl'
        image = '/home/api/Src/test.png'

        pdf = canvas.Canvas(sys.stdout)
        pdf.setPageSize((2970, 2100))
        pdf.setTitle(documentTitle)

        pdf.drawImage(image, 0, 0, 2970, 2100)

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Times-Bold", 100)
        pdf.drawString(1160,1030, name)

        return [True, {"Content": pdf.getpdfdata().decode('utf8', 'ignore'), "Type": "pdf"}, None]

    def ret_bin(self, delete = False):
        ret = ""
        if self.filename is not None:
            if not os.path.exists("/home/api/" + self.filename):
                return [False, "file does not exist", 404]
            with open("/home/api/" + self.filename, 'rb') as f:
                lines = [l.decode('utf8', 'ignore') for l in f.readlines()]
            for i in lines:
                ret += i
            f.close()
            if delete is True:
                os.remove("/home/api/" + self.filename)
        return [True, {"Content": ret.replace('\\n', '\n'), "Type": "pdf"}, None]

    def __getsecret(self):
        return str(os.getenv('API_SCRT', '!@ws4RT4ws212@#%'))
