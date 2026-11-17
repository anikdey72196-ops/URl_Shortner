from django.test import TestCase
from django.urls import reverse
from .models import link

class URLShortenerTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shorten_form.html')

    def test_root_redirects_to_home(self):
        response = self.client.get(reverse('shorten'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_create_short_url(self):
        long_url = 'https://example.com/test'
        response = self.client.post(reverse('shorten'), {'URl': long_url})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(link.objects.filter(Long_url=long_url).exists())
        created_link = link.objects.get(Long_url=long_url)
        self.assertIn(created_link.Short_url, response.content.decode())

    def test_create_short_url_empty_returns_bad_request(self):
        response = self.client.post(reverse('shorten'), {'URl': ''})
        self.assertEqual(response.status_code, 400)

    def test_redirect_to_long_url_and_clicks_increment(self):
        test_link = link.objects.create(
            Long_url='https://example.com/target',
            Short_url='abcd1234'
        )
        self.assertEqual(test_link.click, 0)

        response = self.client.get(reverse('redirect', args=[test_link.Short_url]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, test_link.Long_url)

        test_link.refresh_from_db()
        self.assertEqual(test_link.click, 1)

    def test_nonexistent_short_url_returns_404(self):
        response = self.client.get(reverse('redirect', args=['notfound']))
        self.assertEqual(response.status_code, 404)

