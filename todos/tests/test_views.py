import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Todo
from ..serializers import TodoSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


# initialize the APIClient app
# user = User.objects.get(username='lauren')
client = APIClient()
# client.force_authenticate(user=user)

class getAllTodosTests(TestCase):
    "Test module for get all todos API"

    def setUp(self):
        user = User.objects.create_user('username', 'email', 'password')
        token = Token.objects.get(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # self.username = 'askerTest'
        # self.email = 'askerTest@gmail.com'
        # self.user = User.objects.create_user('username', 'email', 'password')
        # self.token = Token.objects.get(user=user)
        # self.api_authentication()
        
        Todo.objects.create(message="Buy milk", user=self.user)
        Todo.objects.create(message="Buy rice", user=self.user)
        Todo.objects.create(message="Buy chocolate", user=self.user)
   
    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_all_todos(self):
        #get API response
        response = client.get(reverse('get_post_todo'))
        #get data from db
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateTodoTest(TestCase):
    "Test module for inserting a new todo"

    def setUp(self):
        # self.username = 'askerTest'
        # self.email = 'askerTest@gmail.com'
        # self.user = User.objects.create_user(self.username, self.email, 'password')
        # self.token = Token.objects.get(user__username='askerTest')
        # self.api_authentication()
        
        self.valid_todo = {
            'message':'Buy milk'
        }

        self.invalid_todo = {
            'message':''
        }
    
    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_create_valid_todo(self):
        response =  client.post(reverse('get_post_todo'), 
                                data=json.dumps(self.valid_todo),
                                content_type = 'application/json'
                                )
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_todo(self):
        response = client.post(reverse('get_post_todo'),
                               data = json.dumps(self.invalid_todo),
                               content_type = 'application/json' 
                              )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateTodoTest(TestCase):
    "Test module for updating a todo"

    def setUp(self):
        # self.username = 'askerTest'
        # self.email = 'askerTest@gmail.com'
        # self.user = User.objects.create_user(self.username, self.email, 'password')
        # self.token = Token.objects.get(user__username='askerTest')
        # self.api_authentication()

        self.todo_chocolate = Todo.objects.create(message='Buy Chocolate')
        self.valid_todo = {
            'message':'Buy milk'
        }

        self.invalid_todo = {
            'message':''
        }
    
    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_update_valid_todo(self):
        response = client.put(reverse('delete_update_todo', 
                                kwargs={'pk':self.todo_chocolate.pk}),
                                data = json.dumps(self.valid_todo),
                                content_type='application/json'
                            )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_todo(self):
        response = client.put(reverse('delete_update_todo', 
                                kwargs={'pk':self.todo_chocolate.pk}),
                                data = json.dumps(self.invalid_todo),
                                content_type='application/json'
                            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class deleteTodoTest(TestCase):
    "Test module for deleting a todo"

    def setUp(self):
        # self.username = 'askerTest'
        # self.email = 'askerTest@gmail.com'
        # self.user = User.objects.create_user(self.username, self.email, 'password')
        # self.token = Token.objects.get(user__username='askerTest')
        # self.api_authentication()

        self.todo_chocolate = Todo.objects.create(message='Buy chocolate')

    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_delete_valid_todo(self):
        response = client.delete(reverse('delete_update_todo', kwargs={'pk': self.todo_chocolate.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_todo(self):
        response = client.delete(reverse('delete_update_todo', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)