from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer

@api_view(['DELETE', 'PUT'])
def delete_update_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # delete a single todo
    if request.method == 'DELETE':
        return Response({})
    #  update of a single todo
    elif request.method == 'PUT':
        return Response({})

@api_view(['GET', 'POST'])
def get_post_todo(request):
    # get all todos
    if request.method == 'GET':
        return Response({})
    # insert a new record for a todo
    elif request.method == 'POST':
        return Response({})
    


