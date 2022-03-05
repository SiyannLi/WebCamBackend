import datetime
import os
import time
from threading import Thread

import cv2
from flask import Flask, Response, request, make_response, jsonify
from flask_apscheduler import APScheduler
from flask_cors import CORS

from Camera import Camera
from Config import Config

# initialize
app = Flask(__name__, template_folder='./templates')
CORS(app, supports_credentials=True)

camera = Camera()
frame_stream = None
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

@app.route('/')
def welcome_page():
    return "Welcome to TECO lab system!"

@app.route('/change_resolution', methods=['POST', 'GET'])
def change_resolution():
    global current_resolution
    current_resolution = request.json.get("resolution")
    dic = {"status": "success", "code": 200, "current_resolution": current_resolution}
    res = make_response(jsonify(dic))
    return res


@app.route('/get_resolution', methods=['POST', 'GET'])
def get_resolution():
    global current_resolution
    dic = {"status": "success", "code": 200, "current_resolution": current_resolution}
    res = make_response(jsonify(dic))
    return res


@app.route('/change_max_download_time', methods=['POST', 'GET'])
def change_max_download_time():
    global max_download_time
    max_download_time = request.json.get("max_download_time")
    print(max_download_time)
    dic = {"status": "success", "code": 200, "max_download_time": max_download_time}
    res = make_response(jsonify(dic))
    return res


@app.route('/get_max_download_time', methods=['POST', 'GET'])
def get_max_download_time():
    global max_download_time
    dic = {"status": "success", "code": 200, "max_download_time": max_download_time}
    res = make_response(jsonify(dic))
    return res


@app.route('/640')
def video_640():
    global current_resolution
    if current_resolution != 640:
        return 'resolution incorrect, you can only view resolution of %d' % current_resolution, 404, []
    else:
        frame_stream = camera.gen_frames640()
        return Response(frame_stream, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/1920')
def video_1920():
    if current_resolution != 1920:
        return 'resolution incorrect, you can only view resolution of %d' % current_resolution, 404, []
    else:
        frame_stream = camera.gen_frames1920()
        return Response(frame_stream, mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/capture')
# def capture():
#     thread = Thread(target=camera.capture())
#     thread.start()
#     return Response('success')


# @app.route('/video_list')
# def video_list():
#     video_path = '../videos'
#     files = os.listdir(video_path)
#     return Response(files)


@app.route('/download', methods=['POST', 'GET'])
def download():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    print("download")
    print(start_time)
    print(end_time)
    # download one certain video to front end
    camera.cut_video(start_time, end_time)

    def send_file(file_path):
        if not os.path.exists(file_path):
            raise "File not found"
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(10 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    file_path = '../videos/download.avi'
    now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    response = Response(
        send_file(file_path), content_type="application/octet-stream")
    response.headers["Content-disposition"] = 'attachment; filename = %s.avi' % now
    # os.remove(file_path)
    return response


def delete_useless_video():
    now = datetime.datetime.now()
    befor_yes = now - datetime.timedelta(days=2)
    syes = befor_yes.strftime('%Y_%m_%d')
    video_name = os.path.sep.join(['../videos', "{}.avi".format(str(syes))])
    try:
        os.remove(video_name)
    except FileNotFoundError as e:
        pass

def record():
    thread = Thread(camera.record())
    thread.start()


def create_app():
    global current_resolution, max_download_time, frame_stream
    max_download_time = 1000
    current_resolution = 640
    frame_stream = camera.gen_frames640()
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()


create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')

camera.camera.release()
cv2.destroyAllWindows()
