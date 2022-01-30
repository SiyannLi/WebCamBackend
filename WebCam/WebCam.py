from flask import Flask, render_template, Response, request
import cv2
import datetime
import time
import os
import sys
import numpy as np
from threading import Thread


global capture, rec_frame, grey, switch, neg, face, rec, out  # out 视频流
capture = 0  # 截屏
grey = 0  # 灰度图像
neg = 0  # 反转
face = 0  # 人脸检测
switch = 1  # 开关
rec = 0  # 录屏

# make shots directory to save pics
try:
    os.mkdir('../shots')
except OSError as error:
    pass

# make videos directory to save pics
try:
    os.mkdir('../videos')
except OSError as error:
    pass

# Load pretrained face detection model
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt',
                               './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

# instatiate flask app
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(1)


def record(out):
    global rec_frame, switch, camera
    current_switch = switch
    if (switch == 0):
        camera = cv2.VideoCapture(1)
        switch = 1
    while (rec):
        time.sleep(0.05)
        out.write(rec_frame)
    if (current_switch == 0):
        switch = 0
        camera.release()
        cv2.destroyAllWindows()


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:
        return frame

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame = frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = (int(w * r), 480)
        frame = cv2.resize(frame, dim)
    except Exception as e:
        pass
    return frame


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if (face):
                frame = detect_face(frame)
            if (grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if (neg):
                frame = cv2.bitwise_not(frame)
            if (capture):
                capture = 0
                # now = datetime.datetime.now()
                now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now))])
                cv2.imwrite(p, frame)

            if (rec):
                rec_frame = frame
                frame = cv2.putText(cv2.flip(frame, 1), "Recording...", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 4)
                frame = cv2.flip(frame, 1)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
        elif request.form.get('grey') == 'Grey':
            global grey
            grey = not grey
        elif request.form.get('neg') == 'Negative':
            global neg
            neg = not neg
        elif request.form.get('face') == 'Face Only':
            global face
            face = not face
            if (face):
                time.sleep(4)
        elif request.form.get('stop') == 'Stop/Start':

            if (switch == 1):
                switch = 0
                camera.release()
                cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(1)
                switch = 1
        elif request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec = not rec
            if (rec):
                now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                p = os.path.sep.join(['videos', "{}.avi".format(str(now))])
                out = cv2.VideoWriter(p, fourcc, 20.0, (640, 480))
                # Start new thread for recording the video
                thread = Thread(target=record, args=[out, ])
                thread.start()
            elif (rec == False):
                out.release()

    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/video_list')
def video_list():
    video_path = '../videos'
    files = os.listdir(video_path)
    response = Response(files)
    return response

@app.route('download_video')
def download_video():
    # download one certain video to front end
    video_name = request.form.get("video_name")
    video_path = 'video/'+video_name
    def send_file():
        if not os.path.exists(video_path):
            raise "File not found"
        with open(video_path, "rb") as f:
            while True:
                chunk = f.read(10 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk
        response = Response(
            send_file(), content_type="application/octet-stream")
        response.headers["Content-disposition"] = 'attachment; filename = %s' % video_name
        return response


if __name__ == '__main__':
    app.run()

camera.release()
cv2.destroyAllWindows()
