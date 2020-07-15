import requests
from random import randint as ri
from PIL import Image
import json
import os

#Download поля генерируемого для проекции
url='http://127.0.0.1:5000/field_dowload'
rq = requests.get(url=url)
with open('field.png','wb') as req:
    req.write(rq.content)
req = Image.open('field.png')
req.show()
print(f'Status {rq.status_code}')
if rq:
    print('Success')
else:
    print('Failure')
print(f'Time {rq.elapsed.total_seconds()}\n\n')

#Запрос измененных ячеек с последнего запроса расположения
url='http://127.0.0.1:5000/changed_markers_pos'
rq = requests.get(url=url)
print(f'Status {rq.status_code}')
print(f'Data {rq.json()}')
print(f'Time {rq.elapsed.total_seconds()}\n\n')

#Download картинок всех маркеров на поле
url='http://127.0.0.1:5000/marker_dowload_all'
time = 0
rq = requests.get(url=url)
time += rq.elapsed.total_seconds()
for i in range(12):
    try:
        os.remove('mark'+str(i+1)+'.png')
    except:
        a = 0
url='http://127.0.0.1:5000/marker_dowload_all_redirecting'
for i in range(int(rq.content)):
    num = {'num':i}
    req = requests.get(url=url, json=num)
    time += req.elapsed.total_seconds()
    with open('mark'+str(i+1)+'.png','wb') as reqI:
        reqI.write(req.content)
        reqI = Image.open('mark'+str(i+1)+'.png')
        reqI.show()
print(f'Status {rq.status_code}')
if rq:
    print('Success')
else:
    print('Failure')
print('Time ',time,'\n\n')

#Upload внешнего вида маркера, видимого пользователю 
url='http://127.0.0.1:5000/marker_upload'
file = {'file':open('yellow.jpg','rb')}
id = {'id':ri(0,6)}
rq = requests.post(url=url, files=file, data=id)
print(f'Status {rq.status_code}')
if rq:
    print('Success')
else:
    print('Failure')
print(f'Time {rq.elapsed.total_seconds()}\n\n')

#Download картинки ячейки по координатам (не поля)
url='http://127.0.0.1:5000/marker_dowload'
coords = {'coordinates':[2,3]}
rq = requests.get(url=url, json=coords)
with open('newfile.jpg','wb') as req:
    req.write(rq.content)
req = Image.open('newfile.jpg')
req.show()
print(f'Status {rq.status_code}')
if rq:
    print('Success')
else:
    print('Failure')
print(f'Time {rq.elapsed.total_seconds()}\n\n')

#Запрос поворота маркеров
url='http://127.0.0.1:5000/markers_rotate'
markers = {}
for i in range(ri(1,10)):
    x,y,angle=ri(0,7),ri(0,9),ri(-5,5)
    markers.update({i+1:[x,y,angle]})
markers = {'markers':markers}
rq = requests.get(url=url, json=markers)
print(f'Status {rq.status_code}')
print(f'Data {rq.json()}')
print(f'Time {rq.elapsed.total_seconds()}\n\n')

#Запрос расположения маркеров 
url='http://127.0.0.1:5000/markers'
rq = requests.get(url=url)
print(f'Status {rq.status_code}')
print(f'Data {rq.json()}')
print(f'Time {rq.elapsed.total_seconds()}\n\n')