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
        serializer = TodoSerializer(todo, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_post_todo(request):
    # get all todos
    if request.method == 'GET':
        todos = Todo.objects.all()
        serealizer = TodoSerializer(todos, many=True)
        return Response(serealizer.data)
    # insert a new record for a todo
    elif request.method == 'POST':
        data = {
            'message': request.data.get('message')
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


