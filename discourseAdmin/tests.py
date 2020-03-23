from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse


from discourseAdmin.models import User


class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('user-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        response = self.client.post(reverse('user-list'), {})
        self.assertContains(response, '"success": true')

        # Read instance
        items = User.objects.all()
        self.failUnlessEqual(items.count(), 1)
        item = items[0]
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



from discourseAdmin.models import Groups


class GroupsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('groups-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        response = self.client.post(reverse('groups-list'), {})
        self.assertContains(response, '"success": true')

        # Read instance
        items = Groups.objects.all()
        self.failUnlessEqual(items.count(), 1)
        item = items[0]
        response = self.client.get(reverse('groups-details', kwargs={'id': item.id}))
        self.failUnlessEqual(response.status_code, 200)

        # Update instance
        response = self.client.post(reverse('groups-details', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')

        # Delete instance
        response = self.client.post(reverse('groups-delete', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')
        items = Groups.objects.all()
        self.failUnlessEqual(items.count(), 0)



from discourseAdmin.models import User_Groups


class User_GroupsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('user_groups-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        response = self.client.post(reverse('user_groups-list'), {})
        self.assertContains(response, '"success": true')

        # Read instance
        items = User_Groups.objects.all()
        self.failUnlessEqual(items.count(), 1)
        item = items[0]
        response = self.client.get(reverse('user_groups-details', kwargs={'id': item.id}))
        self.failUnlessEqual(response.status_code, 200)

        # Update instance
        response = self.client.post(reverse('user_groups-details', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')

        # Delete instance
        response = self.client.post(reverse('user_groups-delete', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')
        items = User_Groups.objects.all()
        self.failUnlessEqual(items.count(), 0)

