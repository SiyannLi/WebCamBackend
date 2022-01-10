import os
import time
import cv2


class Camera:

    def __init__(self):
        self.camera_opened = None
        self.camera_number = 1
        self.camera = cv2.VideoCapture(self.camera_number)
        self.is_recording = False
        self.camera_opened = False
        # common resources
        self.frame = None
        self.stream_frame = None  # in function gen_frames()

    def gen_frames(self):  # generate frame by frame from camera
        if not self.camera_opened:
            self.camera = cv2.VideoCapture(self.camera_number)
        while True:
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened:
                try:
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
            self.camera = cv2.VideoCapture(self.camera_number)
            self.camera_opened, self.frame = self.camera.read()
        now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        p = os.path.sep.join(['shots', "shot_{}.png".format(str(now))])
        cv2.imwrite(p, self.frame)

    def record(self):# record for ten minutes
        if not self.camera_opened:
            self.camera = cv2.VideoCapture(self.camera_number)
        self.is_recording = True
        now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.sep.join(['videos', "{}.avi".format(str(now))])
        out = cv2.VideoWriter(p, fourcc, 20, (640,480))
        counter = 0
        while self.camera.isOpened():
            self.camera_opened, self.frame = self.camera.read()
            if self.camera_opened and counter < 20*60*10:
                counter += 1
                out.write(self.frame)
            else:
                self.is_recording = False
                break

    # def stop_record(self):
    #     self.is_recording = False
