from fastapi import FastAPI, HTTPException

from Database import Database


# https://github.com/mammothfactory/mammoth_backend/blob/main/parcelapi/views.py
# https://regrid.com/api


# https://app.regrid.com/store/us/fl/jackson

https://www.mapbox.com

# https://support.regrid.com/api/parcel-api-endpoints
PARAMS = {'parcelnumb':parcel_id, 'token':settings.PARCEL_TOKEN, 'limit':1000, 'context':'/us/fl/'}
PARAMS = {'parcelnumb':parcel_id, 'token':settings.PARCEL_TOKEN, 'limit':1000, 'place paths':'/us/fl/jackson'}
r = requests.get(url = settings.PARCEL_URL, params = PARAMS)
resp_data = {'data':r.json()}