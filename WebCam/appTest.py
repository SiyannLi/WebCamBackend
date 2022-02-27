import json
import unittest

from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_stream640(self):
        ret = self.client.get('/640')
        self.assertIsNotNone(ret.data)

    def test_stream1920(self):
        ret = self.client.get('/1920')
        self.assertIsNotNone(ret.data)

    def test_change_resolution(self):
        ret = self.client.get('/change_resolution', data={"resolution": 640})
        resp_json = ret.data
        resp_dict = json.loads(resp_json)
        code = resp_dict.get("code")
        self.assertEqual(code, 200)

if __name__ == '__main__':
    unittest.main()
