from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from todolists.views import home_page
from django.template.loader import render_to_string
from todolists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home_page.html')

    def test_homepage_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/unique-list/')

    def test_homepage_only_saves_item_when_prompted(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first ever list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved = saved_items[0]
        second_saved = saved_items[1]
        self.assertEqual(first_saved.text, 'The first ever list item')
        self.assertEqual(second_saved.text, 'The second list item')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('lists/unique-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_shows_all_items(self):
        Item.objects.create(text='Get some sleep')
        Item.objects.create(text='Wake up')

        response = self.client.get('lists/unique-list/')

        self.assertContains(response, 'Get some sleep')
        self.assertContains(response, 'Wake up')