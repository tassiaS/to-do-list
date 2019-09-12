from django.test import TestCase
from ..models import Todo
from django.contrib.auth.models import User


class TodoTest(TestCase):
    """ Test module for Todo model """

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        Todo.objects.create(
            message='Buy fruits', user=user)
        Todo.objects.create(
            message='Buy rice', user=user)

    def test_todo_message(self):
        todo_fruits = Todo.objects.get(message='Buy fruits')
        todo_rice = Todo.objects.get(message='Buy rice')
        self.assertEqual(
            todo_fruits.completed, False)
        self.assertEqual(
            todo_rice.completed, False)
