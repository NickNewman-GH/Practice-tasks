import json
from random import randint as ri
from flask import Flask, send_file, request as frequest
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, I am glad to see you!'

#Download поля генерируемого для проекции
@app.route('/field_dowload')
def field_dowload():
    return send_file('field.png', mimetype='image/png')

#Запрос измененных ячеек с последнего запроса расположения
@app.route('/changed_markers_pos')
def changed():
    markers=[]
    xlim, ylim, id_lim = 7,9,6
    for i in range(ri(1,10)):
        x, y = ri(0,xlim), ri(0,ylim)
        markers.append({'X':x,'Y':y,'change':'change'})
    return json.dumps({'Markers':markers})

#Download картинок всех маркеров на поле
@app.route('/marker_dowload_all')
def marker_dowload_all():
    number_of_markers = ri(1,8)
    return str(number_of_markers)

@app.route('/marker_dowload_all_redirecting')
def marker_dowload_all_redirecting():
    num = frequest.json.get('num')
    return send_file('pic'+str(num+1)+'.png', mimetype='image/png')

#Upload внешнего вида маркера, видимого пользователю 
@app.route('/marker_upload', methods=['GET', 'POST'])
def marker_upload():
    if frequest.method == 'POST':
        inform = frequest.files['file']
        image = inform.stream._file
        id = int(frequest.form.get('id'))
        decode_img = cv2.imdecode(np.frombuffer(image.getbuffer(), np.uint8), -1)
        cv2.imwrite('marker_img.png',decode_img)
        req = Image.open('marker_img.png')
        req.show()
    return 'Success'

#Download картинки ячейки по координатам (не поля)
@app.route('/marker_dowload')
def marker_dowload():
    coords = frequest.json.get('coordinates')
    img = Image.open('fieldTr.png')
    width, height = img.size
    img = img.crop((width/8*coords[0],height/10*coords[1],width/8*coords[0]+width/8,height/10*coords[1]+height/10))
    img.save('marker.png')
    return send_file('marker.png', mimetype='image/png')

#Запрос поворота маркеров
@app.route('/markers_rotate')
def markers_rotate():
    field=[]
    for i in range(10):
        field.append([])
        for j in range(8):
            field[i].append(ri(0,1))
    markers = frequest.json.get('markers')
    markers_values = []
    status = []
    for i in range(len(markers)):
        markers_values.append(markers[str(i+1)])
    for i in range(len(markers_values)):
        if field[markers_values[i][1]][markers_values[i][0]]==1:
            status.append({'№':i+1,'Status':'Success'})
        else:
            status.append({'№':i+1,'Status':'Failure'})
    return json.dumps({'Status':status})

#Запрос расположения маркеров
@app.route('/markers')
def markers():
    markers=[]
    xlim, ylim, id_lim = 7,9,6
    for i in range(10):
        for j in range(8):
            marker=ri(0,9)
            if marker==0:
                x, y, id = ri(0,xlim), ri(0,ylim), ri(0,id_lim)
                markers.append({'X':x,'Y':y,'ID':id})
    return json.dumps({'markers':markers})

if __name__ == '__main__':
    app.run()