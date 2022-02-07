from flask import Flask, render_template, Response, request, abort
import cv2
import os
from threading import Thread
from Camera import Camera
from Config import Config
from flask_apscheduler import APScheduler

# initialize
app = Flask(__name__, template_folder='./templates')
global current_resolution
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
@app.route('/change_resolution', methods=['POST'])
def change_resolution():
    global current_resolution
    current_resolution = request.json.get("resolution")
    print('change resolution to: ')
    print(current_resolution)
    return Response('succeed')
@app.route('/')
def video_feed():
    global current_resolution
    if current_resolution != 640:
        return Response('resolution incorrect')
    else:
        frame_stream = camera.gen_frames640()
        return Response(frame_stream, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/1920')
def video_1920():
    if current_resolution != 1920:
        return Response('resolution incorrect')
    else:
        frame_stream = camera.gen_frames1920()
        return Response(frame_stream, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture')
def capture():
    thread = Thread(target=camera.capture())
    thread.start()
    return Response('success')


@app.route('/video_list')
def video_list():
    video_path = '../videos'
    files = os.listdir(video_path)
    return Response(files)


@app.route('/download')
def download():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
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
    response = Response(
        send_file(file_path), content_type="application/octet-stream")
    response.headers["Content-disposition"] = 'attachment; filename = %s' % file_path
    return response


@app.route("/record")
def record():
    thread = Thread(camera.record())
    thread.start()


def cron():
    print("testtesttest")


if __name__ == '__main__':
    global current_resolution
    current_resolution = 640
    frame_stream = camera.gen_frames640()

    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()

camera.camera.release()
cv2.destroyAllWindows()
