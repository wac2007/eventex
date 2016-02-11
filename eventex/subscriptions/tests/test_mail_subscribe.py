from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Wallace Coelho', cpf='12345678901', email='wac.almeida@gmail.com', phone='21-1234-5678')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]


    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'wac.almeida@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Wallace Coelho',
            '12345678901',
            'wac.almeida@gmail.com',
            '21-1234-5678'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)