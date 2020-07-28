from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from discourseAdmin.models import User, dGroup, Participant
from discourseAdmin.logic import Utils

class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', is_active=True, is_staff=True)
        self.user.set_password("test_password")
        self.user.save()
        p = Participant(user = self.user)
        p.save();

        logged_in = self.client.login(username='test_user', password="test_password")
        #print(logged_in)

        self.other_user = User.objects.create(username='test_user_2', is_active=True, is_staff=True)
        self.other_user.set_password("test_password_2")
        self.other_user.save()
        p = Participant(user = self.other_user)
        p.save();

    def tearDown(self):
        self.user.delete()

    def test_change_my_password_logged_in(self):
        
        response = self.client.post(reverse('change_password'), {"new_password":"juppi_jokut_1", "repeat_new_password":"juppi_jokut_1"})
        #messages = list(response.context['messages'])
        #for m in messages : print (m)
        logged_in = self.client.login(username='test_user', password="juppi_jokut_1")
        #print(logged_in)
        self.assertTrue(logged_in)


    def test_change_user_password(self):
        new_password = "6tdu.fhknsf.," #muss ausreichend lang sein
        response = self.client.post(reverse("change_user_password", args=[self.other_user.id]), {"username":"test_user_2", "password":"test_password_2", "new_password":new_password, "repeat_new_password":new_password})
        logged_in = self.client.login(username='test_user_2', password=new_password)
        print(logged_in)    
        self.assertTrue(logged_in)

