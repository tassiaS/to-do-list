from django.test import TestCase
from ..models import Todo


class TodoTest(TestCase):
    """ Test module for Todo model """

    def setUp(self):
        Todo.objects.create(
            message='Buy fruits')
        Todo.objects.create(
            message='Buy rice')

    def test_todo_message(self):
        todo_fruits = Todo.objects.get(message='Buy fruits')
        todo_rice = Todo.objects.get(message='Buy rice')
        self.assertEqual(
            todo_fruits.completed, False)
        self.assertEqual(
            todo_rice.completed, False)
