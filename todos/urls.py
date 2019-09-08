from django.urls import path
from . import views

urlpatterns = [
    path(
        'api/v1/todos/<int:pk>',
        views.delete_update_todo,
        name='delete_update_todo'
    ),
    path(
        'api/v1/todos',
        views.get_post_todo,
        name='get_post_todo'
    )
]