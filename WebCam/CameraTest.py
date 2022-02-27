import unittest
from Camera import Camera
import os
import datetime
import app


class TestCase(unittest.TestCase):

    def setUp(self):
        app.app.config.update(TESTING=True)
        self.camera = Camera()
        self.camera.set_up_camera()

    def test_gen_frames640(self):
        video = self.camera.gen_frames640()
        self.assertIsNotNone(video)

    def test_gen_frames1920(self):
        video = self.camera.gen_frames1920()
        self.assertIsNotNone(video)

    def test_record(self):
        self.camera.record(test=True)
        video_path = '../videos'
        files = os.listdir(video_path)
        self.assertIsNotNone(files)

    def test_cut_video(self):
        start_time = '0_0_00'
        end_time = '0_0_04'
        video_path = '../videos/download.avi'
        self.camera.cut_video(start_time, end_time)
        self.assertTrue(os.path.exists(video_path))

    def test_cut_video_wrong_time(self):
        start_time = '0_0_4'
        end_time = '0_0_0'
        self.assertRaises(Exception, self.camera.cut_video, start_time, end_time)


if __name__ == '__main__':
    unittest.main()
