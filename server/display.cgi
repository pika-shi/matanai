#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3
import urllib2
import random
import json
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=7ada960732ff9210&format=json&count=30'

initlat, initlng = 0, 0

if form.has_key('query'):
    url += '&keyword=' + form['query'].value
elif form.has_key('lat') and form.has_key('lng'):
    initlat, initlng = form['lat'].value, form['lng'].value
    url += '&lat=' + initlat + '&lng=' + initlng
else:
    initlat, initlng = 35.02666, 135.781764
    url += '&lat=' + str(initlat) + '&lng=' + str(initlng)

displaycolor = 'red'
if form.has_key('color'):
    displaycolor = form['color'].value

shops = json.load(urllib2.urlopen(url))['results']['shop']
if (initlat, initlng) == (0, 0):
    initlat, initlng = shops[0]['lat'], shops[0]['lng']

markers = ''
for i, shop in enumerate(shops):
    (color, crowd) = random.choice([('blue', 60), ('yellow', 80), ('red', 100)])
    if displaycolor == 'yellow' and color == 'red': continue
    if displaycolor == 'blue' and color in ('red', 'yellow'): continue
    markers += '''var marker{i} = new google.maps.Marker({{
    position: new google.maps.LatLng({lat}, {lng}),
    map: map,
    icon: icon_{color}
    }});

    var infowindow{i} = new google.maps.InfoWindow({{
    content: "<b>{name}</b><br><img src='{image}' align='left' style='margin: 5px 15px 15px 0px;'/>" +
    "<div style='line-height:130%;padding-top:5px;'>{catch}</div>混雑度: {crowd}%",
    maxWidth: 250
    }});

    google.maps.event.addListener(marker{i}, 'click', function() {{
    infowindow{i}.open(map, marker{i});
    }});

    '''.format(i=i, lat=shop['lat'], lng=shop['lng'], color=color, name=shop['name'],
               image=shop['photo']['pc']['s'], catch=shop['catch'], crowd=crowd)

html = '''Content-type: text/html; charset: utf-8

<!DOCTYPE html>
<html>
<head>
<script src="http://maps.google.com/maps/api/js?v=3&sensor=false&language=ja"
type="text/javascript" charset="UTF-8"></script>
<script type="text/javascript">
var map;
function init() {{
var initlatlng = new google.maps.LatLng({lat}, {lng});

var options = {{
zoom: 17,
minZoom: 16,
maxZoom: 20,
mapTypeId: google.maps.MapTypeId.ROADMAP,
center: initlatlng,
streetViewControl: false
}};

map = new google.maps.Map(document.getElementById("map"), options);

var icon_blue = new google.maps.MarkerImage(
'face_blue50.png',
new google.maps.Size(50, 50),
new google.maps.Point(0,0),
new google.maps.Point(25, 25)
);

var icon_yellow = new google.maps.MarkerImage(
'face_yellow50.png',
new google.maps.Size(50, 50),
new google.maps.Point(0,0),
new google.maps.Point(25, 25)
);

var icon_red = new google.maps.MarkerImage(
'face_red50.png',
new google.maps.Size(50, 50),
new google.maps.Point(0,0),
new google.maps.Point(25, 25)
);

{markers}

infowindow0.open(map, marker0);
}}
</script>
</head>

<body onload="init()">
<div id="map" style="width:320px; height:568px; z-index:0; top:0; left:0;
position:absolute;"></div>
</body>

</html>'''.format(markers=markers, lat=initlat, lng=initlng)

print html
