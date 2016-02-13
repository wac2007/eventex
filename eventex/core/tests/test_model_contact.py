from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Wallace Coelho',
            slug='wallace-coelho',
            photo='http://hbn.link/hb-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(
            speaker = self.speaker,
            kind=Contact.EMAIL,
            value='wac.almeida@gmail.com'
        )

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(
            speaker = self.speaker,
            kind=Contact.PHONE,
            value='123456789'
        )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='wac.almeida@gmail.com')
        self.assertEqual('wac.almeida@gmail.com', str(contact))


class ContactManageTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name = 'Wallace Coelho',
            slug='wallace-coelho',
            photo='http://hbn.link/hb-pic'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='wac.almeida@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='123')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['wac.almeida@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['123']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)