import unittest
import urllib.request
import requests

class TestServer(unittest.TestCase):
    #get all users
    def test_get_users(self):
        resp = requests.get('http://localhost/users')
        self.assertEqual(resp.status_code, 200)

    #get all groups
    def test_get_groups(self):
        resp = requests.get('http://localhost/groups')
        self.assertEqual(resp.status_code, 200)

    #get a user by name
    def test_get_user_name(self):
        resp = requests.get('http://localhost/users/query?name=_gamecontrollerd')
        expected = 'b\"[{\'name\': \'_gamecontrollerd\', \'uid\': \'247\', \'gid\': \'247\', \'comment\': \'Game Controller Daemon\', \'home\': \'/var/empty\', \'shell\': \'/usr/bin/false\'}]\"'
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.content), expected)

    #query missing name
    def test_get_missing_name(self):
        resp = requests.get('http://localhost/users/query?name=megan')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(str(resp.content), "b\'[]\'")

    #get uid that doesn't exist
    def test_get_missing_user_id(self):
        resp = requests.get('http://localhost/users/300')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(str(resp.content), "b\'[]\'")

    #get user by id
    def test_get_user_id(self):
        resp = requests.get('http://localhost/users/74')
        expected = 'b\"[{\'name\': \'_mysql\', \'uid\': \'74\', \'gid\': \'74\', \'comment\': \'MySQL Server\', \'home\': \'/var/empty\', \'shell\': \'/usr/bin/false\'}]\"'
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.content), expected)

    #get groups a user belongs to
    def test_get_user_groups(self):
        resp = requests.get('http://localhost/users/33/groups')
        expected = 'b\"[{\'name\': \'_appstore\', \'gid\': \'33\', \'members\': [\'_appstore\']}]\"'
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.content), expected)

    #get group id that doesn't exist
    def test_get_missing_group_id(self):
        resp = requests.get('http://localhost/groups/237')
        self.assertEqual(resp.status_code, 404)

    #test multiple queries
    def test_get_multiple_queries(self):
        resp = requests.get('http://localhost/users/query?uid=247&shell=%2Fusr%2Fbin%2Ffalse')
        expected = 'b\"[{\'name\': \'_gamecontrollerd\', \'uid\': \'247\', \'gid\': \'247\', \'comment\': \'Game Controller Daemon\', \'home\': \'/var/empty\', \'shell\': \'/usr/bin/false\'}]\"'
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.content), expected)

if __name__ == '__main__':
    unittest.main()
