from flask import Flask, render_template, Response, request
import cv2
import os
from threading import Thread
from Camera import Camera
from Config import Config
from flask_apscheduler import APScheduler

# initialize
app = Flask(__name__, template_folder='./templates')

camera = Camera()
frame_stream = None
# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

# make videos directory to save pics
try:
    os.mkdir('./videos')
except OSError as error:
    pass


@app.route('/')
def video_feed():
    return Response(frame_stream, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture')
def capture():
    thread = Thread(target=camera.capture())
    thread.start()
    return Response('success')


@app.route('/video_list')
def video_list():
    video_path = 'videos'
    files = os.listdir(video_path)
    return Response(files)


@app.route('/download')
def download(file_path):
    # download one certain video to front end
    def send_file(file_path):
        if not os.path.exists(file_path):
            raise "File not found"
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(10 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    response = Response(
        send_file(file_path), content_type="application/octet-stream")
    response.headers["Content-disposition"] = 'attachment; filename = %s' % file_path
    return response


def record():
    thread = Thread(camera.record())
    thread.start()


if __name__ == '__main__':
    frame_stream = camera.gen_frames()

    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()

camera.camera.release()
cv2.destroyAllWindows()
