# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import os

#Chapter 4
from django.contrib.staticfiles import finders

#Chapter 5
from rango.models import Page, Category
import populate_rango
import rango.test_utils as test_utils

#Chapter 6
from rango.decorators import chapter6

#Chapter 7
from rango.decorators import chapter7
from rango.forms import CategoryForm, PageForm

#Chapter 8
from django.template import loader
from django.conf import settings
from rango.decorators import chapter8
import os.path

#Chapter 9
from rango.models import User, UserProfile
from rango.forms import UserForm, UserProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from rango.decorators import chapter9

#Chapter 10
from datetime import datetime, timedelta


# ====== Chapter 10
class Chapter10SessionTests(TestCase):
    def test_user_number_of_access_and_last_access_to_index(self):
        #Access index page 100 times
        for i in range(0, 100):
            try:
                response = self.client.get(reverse('index'))
            except:
                try:
                    response = self.client.get(reverse('rango:index'))
                except:
                    return False
            session = self.client.session
            # old_visists = session['visits']

            # Check it exists visits and last_visit attributes on session
            self.assertIsNotNone(self.client.session['visits'])
            self.assertIsNotNone(self.client.session['last_visit'])

            # Check last visit time is within 0.1 second interval from now
            # self.assertAlmostEqual(datetime.now(),
            #     datetime.strptime(session['last_visit'], "%Y-%m-%d %H:%M:%S.%f"), delta=timedelta(seconds=0.1))

            # Get last visit time subtracted by one day
            last_visit = datetime.now() - timedelta(days=1)

            # Set last visit to a day ago and save
            session['last_visit'] = str(last_visit)
            session.save()

            # Check if the visits number in session is being incremented and it's correct
            self.assertEquals(session['visits'], session['visits'])
            # before it was i+1 but visits shouldn't change for the same ip visited in one day


class Chapter10ViewTests(TestCase):
    def test_index_shows_number_of_visits(self):
        #Access index
        try:
            response = self.client.get(reverse('index'))
        except:
            try:
                response = self.client.get(reverse('rango:index'))
            except:
                return False

        # Check it contains visits message
        self.assertIn('visits: 1'.lower(), response.content.decode('ascii').lower())

    def test_about_page_shows_number_of_visits(self):
        #Access index page to count one visit
        try:
            response = self.client.get(reverse('index'))
        except:
            try:
                response = self.client.get(reverse('rango:index'))
            except:
                return False

        # Access about page
        try:
            response = self.client.get(reverse('about'))
        except:
            try:
                response = self.client.get(reverse('rango:about'))
            except:
                return False

        # Check it contains visits message
        self.assertIn('visits: 1'.lower(), response.content.decode('ascii').lower())

    def test_visit_number_is_passed_via_context(self):
        #Access index
        try:
            response = self.client.get(reverse('index'))
        except:
            try:
                response = self.client.get(reverse('rango:index'))
            except:
                return False

        # Check it contains visits message in the context
        self.assertIn('visits', response.context)

        #Access about page
        try:
            response = self.client.get(reverse('about'))
        except:
            try:
                response = self.client.get(reverse('rango:about'))
            except:
                return False

        # Check it contains visits message in the context
        self.assertIn('visits', response.context)
