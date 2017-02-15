from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from todolists.views import home_page
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home_page.html')
        self.assertEqual(response.content.decode(), expected_html)
