from rest_framework.test import APITestCase, override_settings


from auths.models import User
from relationships.models import Relationships


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def user1(self):
        return dict(email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
    def user2(self):
        return dict(email='test2@user.com', username='Testuser2', first_name='Test2',
                    last_name='User2', password='Testuser123', bio='abc2')

    def setUp(self):
        self.client.post('/api/auth/register/', data=self.user1())
        self.client.post('/api/auth/register/', data=self.user2())
        rv1 = self.client.post('/api/auth/login/', data=dict(email=self.user1()['email'],
                                                            password=self.user1()['password']))
        rv2 = self.client.post('/api/auth/login/', data=dict(email=self.user2()['email'],
                                                             password=self.user2()['password']))
        self.user1_db = User.objects.get(username=self.user1()['username'].lower())
        self.user2_db = User.objects.get(username=self.user2()['username'].lower())

        self.auth1 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv1.data['access']}
        self.auth2 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv2.data['access']}

    def test_follow(self):
        #Cannot follow yourself
        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user1()['username'],
                                                              'status': 'FOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 204)
        self.assertEqual(rv.data['status'], 'SELF')

        #Bad rel status
        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'BAD_STATUS'}, **self.auth1)
        self.assertEqual(rv.status_code, 400)

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'FOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 201)
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).first().status == 'FOLLOW'

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'UNFOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).first().status == 'UNFOLLOW'

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'BLOCK'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).first().status == 'BLOCK'

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'UNBLOCK'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user=self.user1_db, to_user=self.user2_db).first().status == 'UNBLOCK'


    def test_get(self):
        #User 1 -> User 2
        rv = self.client.get('/api/relationships/follow/?username='+self.user2()['username'], **self.auth1)
        self.assertEqual(rv.status_code, 204)
        self.assertEqual(rv.data['status'], None)

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user2()['username'],
                                                                  'status': 'FOLLOW'}, **self.auth1)

        rv = self.client.get('/api/relationships/follow/?username=' + self.user2()['username'], **self.auth1)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.data['status'], 'FOLLOW')

        #User 2 -> User 1

        rv = self.client.get('/api/relationships/follow/?username=' + self.user1()['username'], **self.auth2)
        self.assertEqual(rv.status_code, 204)
        self.assertEqual(rv.data['status'], None)

        rv = self.client.post('/api/relationships/follow/', data={'to_user': self.user1()['username'],
                                                                  'status': 'FOLLOW'}, **self.auth2)

        rv = self.client.get('/api/relationships/follow/?username=' + self.user1()['username'], **self.auth2)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.data['status'], 'FOLLOW')





