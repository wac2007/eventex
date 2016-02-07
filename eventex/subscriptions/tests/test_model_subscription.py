from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Wallace Coelho',
            cpf='123',
            email='wac.almeida@gmail.com',
            phone='123'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)