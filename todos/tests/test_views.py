import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Todo
from ..serializers import TodoSerializer


# initialize the APIClient app
client = Client()

class getAllTodosTests(TestCase):
    "Test module for get all todos API"

    def setUp(self):
        Todo.objects.create(message="Buy milk")
        Todo.objects.create(message="Buy rice")
        Todo.objects.create(message="Buy chocolate")

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
        self.valid_todo = {
            'message':'Buy milk'
        }

        self.invalid_todo = {
            'message':''
        }
    
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