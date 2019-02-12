from selenium.webdriver.common.keys import Keys
from rango.models import Category, Page

def login(self):
    self.browser.get(self.live_server_url + '/admin/')

    # Types username and password
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('admin')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('admin')
    password_field.send_keys(Keys.RETURN)

def user_login(self):
    # Types username and password
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('admin')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('admin')
    password_field.send_keys(Keys.RETURN)

def create_categories():
    # List of categories
    categories = []

    # Create categories from 1 to 10
    for i in range(1, 11):
        cat = Category(name="Category " + str(i), likes=i)
        cat.save()
        categories.append(cat)

    return categories

def create_pages(categories):
    # List of pages
    pages = []

    # For each category create 2 pages
    for i in range (0, len(categories)):
        category = categories[i]

        # Name the pages according to the links and create a fake url
        for j in range(0, 2):
            page_number = i * 2 + j + 1
            page = Page(category=category, title="Page " + str(page_number),
                        url="http://www.page" + str(page_number) + ".com", views=page_number)
            page.save()
            pages.append(page)

    return pages

def create_user():
    # Create a user
    from rango.models import User, UserProfile
    user = User.objects.get_or_create(username="testuser", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user,
                                                     website="http://www.testuser.com")[0]
    user_profile.save()

    return user, user_profile
