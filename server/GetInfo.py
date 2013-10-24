#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sys
import sqlite3
import cgi
import cgitb
import json

cgitb.enable()

print 'Content-type: application/json; charset: utf-8'
print

json_list = []
con = sqlite3.connect('matanai.db')
for i in con.execute('select * from beacon').fetchall():
    json_list.append({'id': i[0], 'place': i[1], 'lat': i[2], 'lon': i[3], 'count': i[4]})

print json.dumps({'beacon':json_list})
