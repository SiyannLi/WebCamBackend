import unittest

import WebCam
import os
import time
class TestCase(unittest.TestCase):
    def setUp(self):
        WebCam.app.config.update(TESTING = True)
        

    def test_print_all_files(self):
        print("Hello")
        video_path = 'videos'
        files = os.listdir(video_path)
        for f in files:
            
            print(f)
        #print(files)

    def test_record(self):
        WebCam.new_record()
        time.sleep(5)
        WebCam.new_record()
if __name__ == '__main__':
    unittest.main()