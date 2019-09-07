from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        'api/v1/todos/pk',
        views.delete_update_todo,
        name='delete_update_todo'
    ),
    url(
        'api/v1/todos',
        views.get_post_todo,
        name='get_post_todo'
    )
]