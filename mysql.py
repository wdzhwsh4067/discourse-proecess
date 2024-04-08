# -*- coding: utf-8 -*-
from peewee import *


db = MySQLDatabase('@@@@@', user='root', password='@@@@@@@@@',
                   host='@@@@@@@@', port=3306)

class Novel(Model):
    id = AutoField(primary_key=True)
    title = TextField(null=True)
    title_bbs = TextField(null=True)
    abstract_bbs = TextField(null=True)
    author = TextField(null=True)
    date = DateField(null=True)
    count = DecimalField(max_digits=5, decimal_places=3, null=True)  # Allow up to 5 digits with 3 decimal places
    readtime = DecimalField(max_digits=5, decimal_places=3, null=True)  # Allow up to 5 digits with 3 decimal places
    content = TextField(null=True)
    
    class Meta:
        database = db
        table_name = 'novels'


db.connect()
db.create_tables([Novel])


def insert_data(a,b,c,d,e,f,g,h):
    Novel.create(title=a, author=b, date=c, count=d, readtime=e, content=f,title_bbs=g,abstract_bbs=h)
    return

