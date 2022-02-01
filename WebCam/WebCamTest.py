import unittest
from Camera import Camera
import os
import datetime
import app


class TestCase(unittest.TestCase):

    def setUp(self):
        app.app.config.update(TESTING=True)
        self.camera = Camera()

    def test_print_all_files(self):
        video_path = '../videos'
        files = os.listdir(video_path)
        for f in files:
            print(f)
        # print(files)

    def test_record(self):
        print("record test")
        # camera = Camera()
        self.camera.record()

    def test_time(self):
        start_time = '2022_2_2_1_2_00'
        end_time = '2022_2_2_2_2_00'
        start = datetime.datetime.strptime(start_time, '%Y_%m_%d_%H_%M_%S')
        end = datetime.datetime.strptime(end_time, '%Y_%m_%d_%H_%M_%S')
        start_frame = ((start.hour * 60) + start.minute) * 60 * 20
        end_frame = ((end.hour * 60) + start.minute) * 60 * 20
        print(end_frame-start_frame)

    def test_fileName(self):
        now = datetime.datetime.now()
        yes = now - datetime.timedelta(days=1)
        syes = yes.strftime('%Y_%m_%d')
        input_file = os.path.sep.join(['../videos', "{}.avi".format(str(syes))])
        output_file = os.path.sep.join(['../videos', "{}.avi".format(str('download'))])

        print(input_file)
        print(output_file)

    def test_cut_video(self):
        start_time = '2022_1_31_0_0_00'
        end_time = '2022_1_31_0_0_05'
        self.camera.cut_video(start_time,end_time)

if __name__ == '__main__':
    unittest.main()
