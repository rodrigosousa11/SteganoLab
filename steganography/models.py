from django.db import models
from django.contrib.auth.models import User

class Encoding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to='encodings/')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, default='Encoding')

    def __str__(self):
        return f"Encoding by {self.user.username} at {self.created_at}"

class Decoding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='decodings/')
    message = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, default='Decoding')

    def __str__(self):
        return f"Decoding by {self.user.username} at {self.created_at}"
