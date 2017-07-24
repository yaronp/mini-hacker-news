import json
import unittest

import app


class PostsTest(unittest.TestCase):
    def setUp(self):
        app_instance = app.create_app()
        app.register_routes(app_instance)
        app_instance.testing = True
        self.app = app_instance.test_client()

    def test_Create(self):
        post_text = dict(post="This is my first post!")
        response = self.app.post('/posts', data=json.dumps(post_text), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_Create_empty(self):
        response = self.app.post('/posts', data=json.dumps(""), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_Create_no_body(self):
        response = self.app.post('/posts')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
