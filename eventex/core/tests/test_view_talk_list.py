from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.core.models import Talk, Speaker, Course


class TalkListGet(TestCase):
    def setUp(self):
        t1 = Talk.objects.create(title='Título da Palestra', start='10:00', description='Descrição da Palestra')
        t2 = Talk.objects.create(title='Título da Palestra', start='13:00', description='Descrição da Palestra')
        c1 = Course.objects.create(title='Título do Curso', start='09:00', description='Descrição do Curso', slots=20)

        speaker = Speaker.objects.create(name='Wallace Coelho', slug='wallace-coelho', website='http://wacoelho.com')

        t1.speakers.add(speaker)
        t2.speakers.add(speaker)
        c1.speakers.add(speaker)

        self.resp = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talk_list.html')

    def test_html(self):
        contents = [
            (2, 'Título da Palestra'),
            (1, '10:00'),
            (1, '13:00'),
            (3, '/palestrantes/wallace-coelho'),
            (3, 'Wallace Coelho'),
            (2, 'Descrição da Palestra'),
            (1, 'Título do Curso'),
            (1, '09:00'),
            (1, 'Descrição do Curso')
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_context(self):
        variables = ['morning_talks', 'afternoon_talks']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.resp.context)


class TalkListGetEmpty(TestCase):
    def test_get_empty(self):
        resp = self.client.get(r('talk_list'))

        self.assertContains(resp, 'Ainda não existem palestras de manhã.')
        self.assertContains(resp, 'Ainda não existem palestras de tarde.')