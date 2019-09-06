from django.db import models

class Todo(models.Model):
    message = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

def get_message(self):
    return self.message