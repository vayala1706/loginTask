from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Se establece en la fecha y hora actuales cuando se crea
    updated_at = models.DateTimeField(auto_now=True)      # Se actualiza en la fecha y hora actuales cada vez que se guarda

    def __str__(self):
        return f'{self.title}, {self.content}'
