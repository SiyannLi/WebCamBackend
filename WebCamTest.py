import unittest
from Camera import Camera
import os
import app


class TestCase(unittest.TestCase):

    def setUp(self):
        app.app.config.update(TESTING=True)

    def test_print_all_files(self):
        print("Hello")
        video_path = 'videos'
        files = os.listdir(video_path)
        for f in files:
            print(f)
        # print(files)

    def test_record(self):
        camera = Camera()
        camera.record()


if __name__ == '__main__':
    unittest.main()
