import requests
import json

query_start = "https://geocoding.geo.census.gov/geocoder/geographies/" + "address?benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layers=14&format=json&"

address= "street=4600+Silver+Hill+Rd&city=Suitland&state=MD"

full_query = query_start + address
print(full_query)
r = requests.get(full_query)

print(r.json())
parsed = r.json()
parsed = json.loads('{"result":{"input":{"address":{"state":"MD","street":"4600 Silver Hill Rd","city":"Suitland"},"vintage":{"id":"910","isDefault":true,"vintageName":"Census2010_Census2010","vintageDescription":"Census2010 Vintage - Census2010 Benchmark"},"benchmark":{"id":"9","isDefault":false,"benchmarkDescription":"Public Address Ranges - Census 2010 Benchmark","benchmarkName":"Public_AR_Census2010"}},"addressMatches":[{"geographies":{"Census Blocks":[{"BLKGRP":"1","UR":"","OID":210403970691471,"FUNCSTAT":"S","STATE":"24","AREAWATER":0,"NAME":"Block 1084","SUFFIX":"","LSADC":"BK","CENTLON":"-076.9266698","HU100":0,"LWBLKTYP":"L","BLOCK":"1084","BASENAME":"1084","INTPTLAT":"+38.8477828","POP100":0,"MTFCC":"G5040","COUNTY":"033","GEOID":"240338024051084","CENTLAT":"+38.8477828","INTPTLON":"-076.9266698","AREALAND":33460,"OBJECTID":4385889,"TRACT":"802405"}]},"matchedAddress":"4600 Silver Hill Rd, SUITLAND, MD, 20746","coordinates":{"x":-76.92691,"y":38.846542},"tigerLine":{"tigerLineId":"613199520","side":"L"},"addressComponents":{"preDirection":"","preType":"","streetName":"Silver Hill","suffixType":"Rd","toAddress":"4712","preQualifier":"","suffixDirection":"","suffixQualifier":"","fromAddress":"4600","state":"MD","zip":"20746","city":"SUITLAND"}}]}}')
#parsed = json.loads(r.json())

print("------")
print(parsed['result']['addressMatches']['Census Blocks'])
