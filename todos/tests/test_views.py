import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Todo
from ..serializers import TodoSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class GetAllTodosTests(TestCase):
    "Test module for get all todos API"

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        Todo.objects.create(message="Buy milk", user=user)
        Todo.objects.create(message="Buy rice", user=user)
        Todo.objects.create(message="Buy chocolate", user=user)


    def test_get_all_todos(self):
        #get API response
        response = self.client.get(reverse('get_post_todo'))
        #get data from db
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CreateTodoTest(TestCase):
    "Test module for inserting a new todo"

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        
        self.valid_todo = {
            'message':'Buy milk'
        }

        self.invalid_todo = {
            'message':''
        }
    
    def test_create_valid_todo(self):
        response =  self.client.post(reverse('get_post_todo'), 
                                data=json.dumps(self.valid_todo),
                                content_type = 'application/json'
                                )
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_todo(self):
        response = self.client.post(reverse('get_post_todo'),
                               data = json.dumps(self.invalid_todo),
                               content_type = 'application/json' 
                              )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateTodoTest(TestCase):
    "Test module for updating a todo"

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.todo_chocolate = Todo.objects.create(message='Buy Chocolate', user=user)
        self.valid_todo = {
            'message':'Buy milk'
        }

        self.invalid_todo = {
            'message':''
        }
    
    def test_update_valid_todo(self):
        response = self.client.put(reverse('delete_update_todo', 
                                kwargs={'pk':self.todo_chocolate.pk}),
                                data = json.dumps(self.valid_todo),
                                content_type='application/json'
                            )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_todo(self):
        response = self.client.put(reverse('delete_update_todo', 
                                kwargs={'pk':self.todo_chocolate.pk}),
                                data = json.dumps(self.invalid_todo),
                                content_type='application/json'
                            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_owner(self):
        invalid_owner = User.objects.create_user('invalidusername', 'invalidemail', 'password')
        self.client.force_authenticate(user=invalid_owner)
        response = self.client.put(reverse('delete_update_todo', 
                                kwargs={'pk':self.todo_chocolate.pk}),
                                data = json.dumps(self.valid_todo),
                                content_type='application/json'
                            )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DeleteTodoTest(TestCase):
    "Test module for deleting a todo"

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.todo_chocolate = Todo.objects.create(message='Buy chocolate', user=user)
    
    def test_delete_valid_todo(self):
        response = self.client.delete(reverse('delete_update_todo', kwargs={'pk': self.todo_chocolate.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_todo(self):
        response = self.client.delete(reverse('delete_update_todo', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_owner(self):
        invalid_owner = User.objects.create_user('invalidusername', 'invalidemail', 'password')
        self.client.force_authenticate(user=invalid_owner)
        response = self.client.delete(reverse('delete_update_todo', kwargs={'pk': self.todo_chocolate.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)