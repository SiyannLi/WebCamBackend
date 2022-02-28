import json
import os
import unittest

from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_stream640(self):
        ret_code = self.client.get('/640')._status_code
        self.assertEqual(ret_code, 200)

    def test_stream1920(self):
        ret_code = self.client.get('/1920')._status_code
        self.assertEqual(ret_code, 404)

    def test_change_resolution(self):
        ret_data = self.client.post('/change_resolution', content_type='application/json',
                                    data='{"resolution": 640}').get_data(as_text=True)
        dict = json.loads(ret_data)
        code = dict.get("code")
        resolution = dict.get("current_resolution")
        self.assertEqual(code, 200)
        self.assertEqual(resolution, 640)

    def test_get_resolution(self):
        ret_data = self.client.post('/get_resolution').get_data(as_text=True)
        dict = json.loads(ret_data)
        code = dict.get("code")
        self.assertEqual(code, 200)

    def test_change_max_download_time(self):
        ret_data = self.client.post('/change_max_download_time', content_type='application/json',
                                    data='{"max_download_time": 100}').get_data(as_text=True)
        dict = json.loads(ret_data)
        code = dict.get("code")
        max_download_time = dict.get("max_download_time")
        self.assertEqual(code, 200)
        self.assertEqual(max_download_time, 100)

    def test_get_max_download_time(self):
        ret_data = self.client.post('/get_max_download_time').get_data(as_text=True)
        dict = json.loads(ret_data)
        code = dict.get("code")
        self.assertEqual(code, 200)

    def test_download(self):
        ret_code = self.client.get('/download?start_time=0_0_0&end_time=0_0_1')._status_code
        self.assertEqual(ret_code, 200)

    def test_delete_video(self):
        import app as ap
        ap.delete_useless_video()




if __name__ == '__main__':
    unittest.main()
