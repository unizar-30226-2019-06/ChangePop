import unittest
import warnings

from flask import json

import webapp


# from webapp import app
# from webapp import home


class HomeViewTest(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertIn('Home Page', str(home.data))


class UserDataBase(unittest.TestCase):
    tmp_user_id = -1
    user_data = json.dumps({
            "id": 0,
            "nick": "Alice",
            "first_name": "Foo",
            "last_name": "Bar",
            "mail": "mail@email.com",
            "pass": "pass",
            "phone": "666999222",
            "is_mod": True,
            "ban_reason": "Razon expulsion",
            "points": 0,
            "avatar": "http://images.com/235gadfg",
            "fnac": "2019-04-07",
            "dni": "123456789",
            "place": "Madrid",
            "token": "2sf78gsf68hsf5asfh68afh68a58fha68f"
        })
    user_login = json.dumps({
          "nick": "Alice",
          "pass": "pass",
          "remember": True
        })

    user_update = json.dumps({
            "nick": "Alice",
            "first_name": "FooFoo",
            "last_name": "Bar",
            "mail": "mail@email.com",
            "pass": "pass",
            "phone": "666999222",
            "is_mod": True,
            "ban_reason": "Razon expulsion",
            "points": 0,
            "avatar": "http://images.com/235gadfg",
            "fnac": "2019-04-07",
            "dni": "123456789",
            "place": "Madrid",
            "token": "2sf78gsf68hsf5asfh68afh68a58fha68f",
            "pass_hash": "s32uh5423j5h23jh52jh35"
        })

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_1_add_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=self.user_data, mimetype='application/json').get_json()
            self.assertIn('info', str(r_json))  # Check successful insertion

            user_id = r_json["message"]
            self.__class__.tmp_user_id = user_id

            check = self.app.get('/profile/Alice')
            self.assertIn('666999222', str(check.get_json()))  # Check get info

    def test_2_session_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/login', data=self.user_login, mimetype='application/json').get_json()
            self.assertIn('Alice', str(r_json))  # Check successful login

            r_json = self.app.get('/user').get_json()
            self.assertIn('Alice', str(r_json))  # Check get logged user info

            r_json = self.app.get('/logout').get_json()  # Logout
            self.assertIn('out', str(r_json))  # Check successful

            r_json = self.app.get('/user').get_json()  # Try get my info
            self.assertIn('Not logged in', str(r_json))  # Check successful

    def test_3_update_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.get('/login', data=self.user_login, mimetype='application/json')  # Login to set the session

            r_json = self.app.put('/user', data=self.user_update, mimetype='application/json').get_json()
            msg = r_json["message"]
            self.assertIn(str(self.__class__.tmp_user_id), msg)  # Check successful update

            r = self.app.get('/user').get_json()
            self.assertIn("FooFoo", str(r))  # Check unsuccessful login

    def test_4_delete_user(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            self.app.get('/login', data=self.user_login, mimetype='application/json')    # Login to set the session

            r_json = self.app.delete('/user').get_json()
            msg = r_json["message"]
            self.assertIn(str(self.__class__.tmp_user_id), msg)  # Check successful deletion

            r = self.app.get('/login', data=self.user_login, mimetype='application/json').get_json()
            self.assertIn("User not found", str(r))  # Check unsuccessful login

    def test_5_mod_users(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            r_json = self.app.post('/user', data=self.user_data, mimetype='application/json').get_json()  # User created
            user_id = r_json["message"]
            self.__class__.tmp_user_id = user_id

            r_json = self.app.post('/user/setmod/'+str(user_id), data=self.user_data, mimetype='application/json').get_json()
            self.assertIn('ok', str(r_json))  # Check set mod

            self.app.get('/login', data=self.user_login, mimetype='application/json')  # Login to set the session

            r_json = self.app.get('/user/'+str(user_id)).get_json()
            self.assertIn('Alice', str(r_json))  # Check get user info

            r_json = self.app.put('/user/'+str(user_id), data=self.user_update, mimetype='application/json').get_json()
            self.assertIn('updated', str(r_json))  # Check update user info

            r_json = self.app.delete('/user/'+str(user_id)).get_json()
            self.assertIn('deleted', str(r_json))  # Check delete user info



class ProductDataBase(unittest.TestCase):
    user_id: int = 1

    def setUp(self):
        self.app = webapp.app.test_client()
        self.app.testing = True

    def test_add_product(self):
        data = {
            "id": 0,
            "descript": "This product is wonderful",
            "user_id": str(self.user_id),
            "price": 0,
            "categories": [
                "Moda"
            ],
            "title": "Producto Molongo",
            "bid": "2019-04-07",
            "boost_date": "2019-04-07",
            "visits": 0,
            "followers": 0,
            "publish_date": "2019-04-07",
            "photo_urls": [
                "http://images.com/123af3"
            ],
            "place": "Zaragoza",
            "is_removed": True,
            "ban_reason": "Razon Baneo"
        }

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            data_send = json.dumps(data)
            response = self.app.post('/product', data=data_send, mimetype='application/json')

            r_json = response.get_json()
            self.assertIn('info', str(response.get_json()))  # Check successful insertion

            product_id = r_json["message"]
            check = self.app.get('/product/' + str(product_id))
            self.assertIn('Zaragoza', str(check.get_json()))  # Check get info


if __name__ == "__main__":
    unittest.main()
