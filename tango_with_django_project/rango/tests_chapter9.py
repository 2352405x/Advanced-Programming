# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import os, socket

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
from selenium.webdriver.common.keys import Keys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from rango.decorators import chapter9

# ===== Chapter 9
class Chapter9LiveServerTests(StaticLiveServerTestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options = chrome_options)
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(Chapter9LiveServerTests, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    @chapter9
    def test_register_user(self):
        #Access index page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')

        try:
            self.browser.get(url + reverse('index'))
        except:
            try:
                self.browser.get(url + reverse('rango:index'))
            except:
                return False

        #Click in Register
        self.browser.find_elements_by_link_text('Sign Up')[0].click()

        # Fill registration form
        # username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('testuser')

        # email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('testuser@testuser.com')

        # password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('test1234')

        # website
        website_field = self.browser.find_element_by_name('website')
        website_field.send_keys('http://www.testuser.com')

        # Submit
        website_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # Check for success message
        self.assertIn('Rango says: thank you for registering!'.lower(), body.text.lower())
        self.browser.find_element_by_link_text('Return to the homepage.')

    def test_admin_contains_user_profile(self):
        # Access admin page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('admin:index'))

        # Log in the admin page
        test_utils.login(self)

        # Check exists a link to user profiles
        self.browser.find_element_by_link_text('User profiles').click()

        # Check it is empty
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 user profiles', body.text)

        # create a user
        user, user_profile = test_utils.create_user()

        self.browser.refresh()

        # Check there is one profile
        body = self.browser.find_element_by_tag_name('body')
        # self.assertIn(user.username, body.text)

    @chapter9
    def test_links_in_index_page_when_logged(self):
        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        #Check links that appear for logged person only
        self.browser.find_element_by_link_text('Add a New Category')
        self.browser.find_element_by_link_text('Restricted Page')
        self.browser.find_element_by_link_text('Logout')
        self.browser.find_element_by_link_text('About')

        # Check that links does not appears for logged users
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Sign In', body.text)
        self.assertNotIn('Sign Up', body.text)

    def test_links_in_index_page_when_not_logged(self):
        #Access index page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('index'))
        except:
            try:
                self.browser.get(url + reverse('rango:index'))
            except:
                return False

        #Check links that appear for not logged person only
        self.browser.find_element_by_link_text('Sign Up')
        self.browser.find_element_by_link_text('Sign In')
        self.browser.find_element_by_link_text('About')

        # Check that links does not appears for not logged users
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Add a New Category', body.text)
        self.assertNotIn('Restricted Page', body.text)
        self.assertNotIn('Logout', body.text)

    @chapter9
    def test_logout_link(self):
        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        #Clicks to logout
        self.browser.find_element_by_link_text('Logout').click()

        # Check if it see log in link, thus it is logged out
        self.browser.find_element_by_link_text('Sign In')

    @chapter9
    def test_add_category_when_logged(self):
        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        # Click category
        self.browser.find_element_by_partial_link_text('Add a New Category').click()

        # Types new category name
        username_field = self.browser.find_element_by_name('name')
        username_field.send_keys('New Category')

        # Click on Create Category
        self.browser.find_element_by_css_selector(
            "input[type='submit']"
        ).click()

        body = self.browser.find_element_by_tag_name('body')

        # Check if New Category appears in the index page
        self.assertIn('New Category', body.text)

    @chapter9
    def test_add_page_when_logged(self):
        #Create categories
        test_utils.create_categories()

        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        # Click category
        self.browser.find_element_by_partial_link_text('Category').click()

        # Click add page
        try:
            self.browser.find_element_by_partial_link_text("Add").click()
        except:
            self.browser.find_element_by_partial_link_text("add").click()

        # Types new page name
        username_field = self.browser.find_element_by_name('title')
        username_field.send_keys('New Page')

        # Types url for the page
        username_field = self.browser.find_element_by_name('url')
        username_field.send_keys('http://www.newpage.com')

        # Click on Create Page
        self.browser.find_element_by_css_selector(
            "input[type='submit']"
        ).click()

        body = self.browser.find_element_by_tag_name('body')

        # Check if New Page appears in the category page
        self.assertIn('New Page', body.text)

    def test_add_page_when_not_logged(self):
        #Create categories
        test_utils.create_categories()

        # Access index
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('index'))
        except:
            try:
                self.browser.get(url + reverse('rango:index'))
            except:
                return False

        # Click category
        self.browser.find_element_by_partial_link_text('Category').click()

        # Check it does not have a link to add page
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Add a Page', body.text)

    @chapter9
    def test_access_restricted_page_when_logged(self):
        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        # Access restricted page
        self.browser.find_element_by_link_text('Restricted Page').click()

        # Check that a message is displayed
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("Since you're logged in, you can see this text!".lower(), body.text.lower())

    def test_access_restricted_page_when_not_logged(self):
        # Access restricted page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('restricted'))
        except:
            try:
                self.browser.get(url + reverse('rango:restricted'))
            except:
                return False

        # Check login form is displayed
        # username
        self.browser.find_element_by_name('username')

        # password
        self.browser.find_element_by_name('password')

    @chapter9
    def test_logged_user_message_in_index(self):
        # Access login page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        try:
            self.browser.get(url + reverse('login'))
        except:
            try:
                self.browser.get(url + reverse('rango:login'))
            except:
                return False

        # Log in
        test_utils.user_login(self)

        # Check for the username in the message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('admin', body.text)


class Chapter9ModelTests(TestCase):
    def test_user_profile_model(self):
        # Create a user
        user, user_profile = test_utils.create_user()

        # Check there is only the saved user and its profile in the database
        all_users = User.objects.all()
        self.assertEquals(len(all_users), 1)

        all_profiles = UserProfile.objects.all()
        self.assertEquals(len(all_profiles), 1)

        # Check profile fields were saved correctly
        all_profiles[0].user = user
        all_profiles[0].website = user_profile.website

class Chapter9ViewTests(TestCase):

    @chapter9
    def test_registration_form_is_displayed_correctly(self):
        #Access registration page
        try:
            response = self.client.get(reverse('register'))
        except:
            try:
                response = self.client.get(reverse('rango:register'))
            except:
                return False

        # Check if form is rendered correctly
        # self.assertIn('<h1>Register with Rango</h1>', response.content.decode('ascii'))
        self.assertIn('<strong>register here!</strong><br />'.lower(), response.content.decode('ascii').lower())

        # Check form in response context is instance of UserForm
        self.assertTrue(isinstance(response.context['user_form'], UserForm))

        # Check form in response context is instance of UserProfileForm
        self.assertTrue(isinstance(response.context['profile_form'], UserProfileForm))

        user_form = UserForm()
        profile_form = UserProfileForm()

        # Check form is displayed correctly
        self.assertEquals(response.context['user_form'].as_p(), user_form.as_p())
        self.assertEquals(response.context['profile_form'].as_p(), profile_form.as_p())

        # Check submit button
        self.assertIn('type="submit"', response.content.decode('ascii'))
        self.assertIn('name="submit"', response.content.decode('ascii'))
        self.assertIn('value="Register"', response.content.decode('ascii'))

    @chapter9
    def test_login_form_is_displayed_correctly(self):
        #Access login page
        try:
            response = self.client.get(reverse('login'))
        except:
            try:
                response = self.client.get(reverse('rango:login'))
            except:
                return False

        #Check form display
        #Header
        self.assertIn('<h1>Login to Rango</h1>'.lower(), response.content.decode('ascii').lower())

        #Username label and input text
        self.assertIn('Username:', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Password label and input text
        self.assertIn('Password:', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Submit button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="submit"', response.content.decode('ascii'))

    @chapter9
    def test_login_form_is_displayed_correctly(self):
        #Access login page
        try:
            response = self.client.get(reverse('login'))
        except:
            try:
                response = self.client.get(reverse('rango:login'))
            except:
                return False

        #Check form display
        #Header
        self.assertIn('<h1>Login to Rango</h1>'.lower(), response.content.decode('ascii').lower())
        
        #Username label and input text
        self.assertIn('Username:', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Password label and input text
        self.assertIn('Password:', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Submit button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="submit"', response.content.decode('ascii'))

    @chapter9
    def test_login_provides_error_message(self):
        # Access login page
        try:
            response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        except:
            try:
                response = self.client.post(reverse('rango:login'), {'username': 'wronguser', 'password': 'wrongpass'})
            except:
                return False

        print(response.content.decode('ascii'))
        try:
            self.assertIn('wronguser', response.content.decode('ascii'))
        except:
            self.assertIn('Invalid login details supplied.', response.content.decode('ascii'))

    @chapter9
    def test_login_redirects_to_index(self):
        # Create a user
        test_utils.create_user()

        # Access login page via POST with user data
        try:
            response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'test1234'})
        except:
            try:
                response = self.client.post(reverse('rango:login'), {'username': 'testuser', 'password': 'test1234'})
            except:
                return False

        # Check it redirects to index
        self.assertRedirects(response, reverse('index'))

    @chapter9
    def test_upload_image(self):
        # Create fake user and image to upload to register user
        image = SimpleUploadedFile("testuser.jpg", b"file_content", content_type="image/jpeg")
        try:
            response = self.client.post(reverse('register'),
                             {'username': 'testuser', 'password':'test1234',
                              'email':'testuser@testuser.com',
                              'website':'http://www.testuser.com',
                              'picture':image } )
        except:
            try:
                response = self.client.post(reverse('rango:register'),
                                 {'username': 'testuser', 'password':'test1234',
                                  'email':'testuser@testuser.com',
                                  'website':'http://www.testuser.com',
                                  'picture':image } )
            except:
                return False

        # Check user was successfully registered
        self.assertIn('thank you for registering!'.lower(), response.content.decode('ascii').lower())
        user = User.objects.get(username='testuser')
        user_profile = UserProfile.objects.get(user=user)
        path_to_image = './media/profile_images/testuser.jpg'

        # Check file was saved properly
        self.assertTrue(os.path.isfile(path_to_image))

        # Delete fake file created
        default_storage.delete('./media/profile_images/testuser.jpg')
