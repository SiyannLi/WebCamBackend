import datetime
import os
import time

import cv2


class Camera:

    def __init__(self):
        self.camera = None
        self.camera_number = 1
        self.str = "rtsp://admin:12345678@10.12.180.110:554//h264Preview_01_sub"
        self.rtmp = "rtmp://10.12.180.110/bcs/channel0_sub.bcs?channel=0&stream=1&user=admin&password=12345678"
        self.mp4 = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
        # self.camera = cv2.VideoCapture(self.rtmp_str)
        self.set_up_camera()
        self.is_recording = False
        self.camera_opened = False
        # common resources
        self.frame = None
        self.stream_frame = None  # in function gen_frames()
        #os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

    def set_up_camera(self):
        #self.camera = cv2.VideoCapture(self.rtmp, cv2.CAP_FFMPEG)
        self.camera = cv2.VideoCapture(self.mp4)

    def gen_frames640(self):  # generate frame by frame from camera
        self.set_up_camera()
        while True:
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened:
                try:
                    self.frame = cv2.resize(self.frame, (640, 360))
                    # self.frame = cv2.flip(self.frame, 180)
                    # ret, buffer = cv2.imencode('.jpg', cv2.flip(self.frame, 1))
                    ret, buffer = cv2.imencode('.jpg', self.frame)

                    stream_frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')
                except Exception as e:
                    pass
            else:
                pass

    def gen_frames1920(self):  # generate frame by frame from camera
        self.set_up_camera()
        while True:
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened:
                try:
                    self.frame = cv2.resize(self.frame, (1920, 1080))
                    # self.frame = cv2.flip(self.frame, 180)
                    # ret, buffer = cv2.imencode('.jpg', cv2.flip(self.frame, 1))
                    ret, buffer = cv2.imencode('.jpg', self.frame)

                    stream_frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')
                except Exception as e:
                    pass
            else:
                pass

    def record(self, test=False):  # record for ten minutes
        day_frames = 10 * 60 * 60 * 7  # every day has these frames from 9:00 - 16:00
        minute_frames = 30 * 60
        if not self.camera_opened:
            self.set_up_camera()
        self.is_recording = True
        now = time.strftime("%Y_%m_%d", time.localtime())
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.sep.join(['../videos', "{}.avi".format(str(now))])
        out = cv2.VideoWriter(p, fourcc, 10, (640, 360))
        counter = 0
        if test:
            day_frames = 150
        while self.camera.isOpened():
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened and counter < day_frames:
                counter += 1
                out.write(self.frame)
            else:
                self.is_recording = False
                break
        out.release()

    def cut_video(self, start_time, end_time):
        now = datetime.datetime.now()
        yes = now - datetime.timedelta(days=1)
        syes = yes.strftime('%Y_%m_%d')
        input_file = os.path.sep.join(['../videos', "{}.avi".format(str(syes))])
        output_file = os.path.sep.join(['../videos', "{}.avi".format(str('download'))])

        if not os.path.exists(input_file):
            raise Exception("The video to be cut does not exist")

        start = datetime.datetime.strptime(start_time, '%H_%M_%S')
        end = datetime.datetime.strptime(end_time, '%H_%M_%S')
        if start.hour < 9:
            raise Exception("Video starts at 9 o'clock")
        if start.hour > 16:
            raise Exception("Video starts at 16 o'clock")
        start_frame = ((start.hour - 9) * 60 * 60 + start.minute * 60 + start.second) * 10
        end_frame = ((end.hour - 9) * 60 * 60 + end.minute * 60 + end.second) * 10

        if end_frame < start_frame:
            raise Exception("End time should not later than start time")
        reader = cv2.VideoCapture(input_file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(output_file, fourcc, 10, (640, 360))

        have_more_frame = True
        c = -1
        while have_more_frame:
            have_more_frame, frame = reader.read()
            c += 1
            if start_frame <= c <= end_frame:
                cv2.waitKey(1)
                writer.write(frame)
            if c > end_frame:
                writer.release()
                reader.release()
                break
