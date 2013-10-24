#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import logging
import cgi
import cgitb

logging.basicConfig(level=logging.INFO,
                    filename='log.txt',
                    format='%(asctime)s %(levelname)s %(message)s')

cgitb.enable()
f = cgi.FieldStorage()

id, status = f['id'].value, f['status'].value

if status == 'in': status = '+'
else: status = '-'

con = sqlite3.connect('matanai.db')
con.execute('update beacon set count = count %s 1 where id = %s' % (status, id))
count = con.execute('select count from beacon where id = %s' % (id)).fetchone()[0]
con.commit()
con.close()

logging.info('id = ' + str(id) + ' count = ' + str(count))

print 'Content-type: text/html; charset: utf-8'
print
