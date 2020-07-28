from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from discourseAdmin.models import User, dGroup
from discourseAdmin.logic import Utils


# erstmal umbenannt so das es nicht automatisch aufgerufen wird
class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', is_active=True, is_staff=True)
        self.user.set_password("test_password")
        self.user.save()
        logged_in = self.client.login(username='test_user', password="test_password")

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('user-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        response = self.client.post(reverse('create_user'), {"username":'test_user_2', "password":"test_password_2"})
        self.failUnlessEqual(response.status_code, 200)
        print(response)

        # Read instance
        items = User.objects.all()
        self.failUnlessEqual(items.count(), 2)
        item = items[0]
        print(item.__dict__)
        response = self.client.get(reverse('user-details', kwargs={'id': item.id}))
        self.failUnlessEqual(response.status_code, 200)

        # Update instance
        response = self.client.post(reverse('user-details', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')

        # Delete instance
        response = self.client.post(reverse('user-delete', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')
        items = User.objects.all()
        self.failUnlessEqual(items.count(), 0)



from discourseAdmin.models import dGroup


class GroupsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', is_active=True, is_staff=True)
        self.user.set_password("test_password")
        self.user.save()
        logged_in = self.client.login(username='test_user', password="test_password")

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('group-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        print("start group-create")

        #groupsDict = client.groups()
        #print(groupsDict)
        response = self.client.post(reverse('group-create'), {"name":"djangotest"})
        #print(response)
        #self.assertContains(response, '"success": true')

        #Read from Discourse
        client = Utils.getDiscourseClient()
        try: 
            discGroups = client.groups()
            assertCG = False;
            for group in discGroups:
                if group['name'] == "djangotest": assertCG = True
            self.assertTrue(assertCG)
        except: self.fail("Gruppe ist nicht in Discourse angekommen")

        # Read instance
        items = dGroup.objects.all()
        self.failUnlessEqual(items.count(), 1)
        item = items[0]
        response = self.client.get(reverse('group-details', kwargs={'id': item.id}))
        self.failUnlessEqual(response.status_code, 200)

        # Delete instance
        response = self.client.post(reverse('group-delete', kwargs={'id': item.id}), {})
        items = dGroup.objects.all()
        self.failUnlessEqual(items.count(), 0)


