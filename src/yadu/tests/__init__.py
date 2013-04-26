from django.test import TestCase
from django.core.urlresolvers import reverse


class XSendFileTests(TestCase):
    def test_xsendfile(self):
        url = reverse('wo_login', args=['miao.png',])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.has_header("X-Sendfile"), True)

    def test_need_login(self):
        url = reverse('w_login', args=['miao.png',])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

class SSLTests(TestCase):
    def test_redirect(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://testserver%s" % url)
