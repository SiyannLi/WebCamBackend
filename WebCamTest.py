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
        WebCam.record_switch()
        time.sleep(5)
        WebCam.record_switch()
if __name__ == '__main__':
    unittest.main()