import datetime
import os
import time
import cv2


class Camera:

    def __init__(self):
        self.camera_opened = None
        self.camera_number = 1
        # self.rtmp_str = 'rtsp://admin:12345678@192.168.1.226:554//h265Preview_01_main'
        # self.camera = cv2.VideoCapture(self.rtmp_str)
        self.set_up_camera()
        self.is_recording = False
        self.camera_opened = False
        # common resources
        self.frame = None
        self.stream_frame = None  # in function gen_frames()

    def set_up_camera(self):
        self.camera = cv2.VideoCapture(self.camera_number)

    def gen_frames(self):  # generate frame by frame from camera
        self.set_up_camera()
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
            self.set_up_camera()
            self.camera_opened, self.frame = self.camera.read()
        now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        p = os.path.sep.join(['../shots', "shot_{}.png".format(str(now))])
        cv2.imwrite(p, self.frame)

    def record(self):  # record for ten minutes
        print("record")
        day_frames = 20 * 60 * 60 * 24  # every day has these frames
        minute_frames = 20 * 60
        if not self.camera_opened:
            self.set_up_camera()
        self.is_recording = True
        now = time.strftime("%Y_%m_%d", time.localtime())
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.sep.join(['../videos', "{}.avi".format(str(now))])
        out = cv2.VideoWriter(p, fourcc, 20, (640, 480))
        counter = 0
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

        start = datetime.datetime.strptime(start_time, '%Y_%m_%d_%H_%M_%S')
        end = datetime.datetime.strptime(end_time, '%Y_%m_%d_%H_%M_%S')
        start_frame = (((start.hour * 60) + start.minute) * 60 + start.second) * 20
        end_frame = (((end.hour * 60) + start.minute) * 60 + end.second) * 20

        reader = cv2.VideoCapture(input_file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(output_file, fourcc, 20, (640, 480))

        have_more_frame = True
        c = -1
        while have_more_frame:
            have_more_frame, frame = reader.read()
            c += 1
            if c >= start_frame and c <= end_frame:
                cv2.waitKey(1)
                writer.write(frame)
            if c > end_frame:
                writer.release()
                reader.release()
                break
