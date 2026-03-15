from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note.'
        )

    def test_note_has_title(self):
        self.assertEqual(self.note.title, 'Test Note')

    def test_note_has_content(self):
        self.assertEqual(self.note.content, 'This is a test note.')

    def test_string_representation(self):
        self.assertEqual(str(self.note), 'Test Note')


class NoteViewTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note.'
        )

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        response = self.client.get(reverse('note_detail', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note.')

    def test_note_create_view(self):
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'New content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 2)
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_note_update_view(self):
        response = self.client.post(reverse('note_update', args=[self.note.id]), {
            'title': 'Updated Note',
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
        self.assertEqual(self.note.content, 'Updated content')

    def test_note_delete_view(self):
        response = self.client.post(reverse('note_delete', args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 0)
