from asyncore import write
from csv import writer
import os
import time
from turtle import width
import cv2


class Camera:

    def __init__(self):
        self.camera_opened = None
        self.camera_number = 1
        self.rtmp_str = 'rtsp://admin:12345678@192.168.1.226:554//h265Preview_01_main'
        self.camera = cv2.VideoCapture(self.rtmp_str)
        self.is_recording = False
        self.camera_opened = False
        # common resources
        self.frame = None
        self.stream_frame = None  # in function gen_frames()

    def gen_frames(self):  # generate frame by frame from camera
        self.camera = cv2.VideoCapture(self.rtmp_str)
        while True:
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened:
                try:
                    self.frame = cv2.resize(self.frame, (640, 480))
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(self.frame, 1))
                    stream_frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')
                except Exception as e:
                    pass

            else:
                pass

    def capture(self):
        if not self.camera_opened:
            self.camera = cv2.VideoCapture(self.rtmp_str)
            self.camera_opened, self.frame = self.camera.read()
        now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        p = os.path.sep.join(['shots', "shot_{}.png".format(str(now))])
        cv2.imwrite(p, self.frame)

    def record(self):  # record for ten minutes
        if not self.camera_opened:
            self.camera = cv2.VideoCapture(self.rtmp_str)
        self.is_recording = True
        now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.sep.join(['videos', "{}.avi".format(str(now))])
        out = cv2.VideoWriter(p, fourcc, 20, (640, 480))
        counter = 0
        while self.camera.isOpened():
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened and counter < 20 * 60 * 10:
                counter += 1
                out.write(self.frame)
            else:
                self.is_recording = False
                break
        out.release()

    # def stop_record(self):
    #     self.is_recording = False
    def cut_video(start_time, end_time):
        input_file = ''
        output_file = ''
        start_frame = 0
        end_frame = 0
        reader = cv2.VideoCapture(input_file)
        width = int(reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))

        have_more_frame = True
        c = -1
        while have_more_frame:
            have_more_frame, frame = reader.read()
            c += 1
            if c >= start_frame and c <= end_frame:
                cv2.waitKey(1)
                writer.write(frame)
            if c > end_frame:
                break

        writer.release()
        reader.release()
