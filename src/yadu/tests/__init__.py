from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from customer.models import (
    Customer,
    ZipCode,
    Address,
)


class XSendFileTests(TestCase):
    def test_xsendfile_wo_login(self):
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

class RelatedFieldAdminTests(TestCase):

    def setUp(self):
        # create the admin user
        admin = User.objects.create(
            username='admin',
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        admin.set_password('password')
        admin.save()

        # create an entry
        zipcode = ZipCode.objects.create(state='Bananas')
        address = Address.objects.create(zip_code=zipcode, street='Carnaby')
        customer = Customer.objects.create(address=address, name='Mr Bean')

    def test_list_field(self):
        url = reverse('admin:customer_customer_changelist')
        self.assertEquals(
            self.client.login(username='admin', password='password'),
            True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
