import sys
from io import BytesIO

import requests
from PIL import Image
from distance import lonlat_distance
from business import find_business
from geocoder import get_ll_coord, get_ll_span

toponym_to_find = 'Добринка Воронского 35'
lat, lon = get_ll_coord(toponym_to_find)
address_ll = f'{lat},{lon}'
span = '0.005,0.005'
organization = find_business(address_ll, span, 'аптека')
point = organization['geometry']['coordinates']
org_lat = float(point[0])
org_lon = float(point[1])
point_param = f'{org_lat},{org_lon},pm2dgl'

points_param = point_param + f'~{address_ll},pm2rdl'
params = {
    'l':'map',
    'pt': points_param
}
map_api_server = 'http://static-maps.yandex.ru/1.x/'
resource = requests.get(map_api_server, params=params)
print(organization['properties']['CompanyMetaData']['name'])
print(organization['properties']['CompanyMetaData']['address'])
print(organization['properties']['CompanyMetaData']['Hours']['text'])
print(round(lonlat_distance((lat, lon), tuple(organization["geometry"]["coordinates"]))))
Image.open(BytesIO(resource.content)).show()
