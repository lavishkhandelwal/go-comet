import json
from django.db import models

# Create your models here.
class Tags(models.Model):
    tags = models.CharField(max_length = 30)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.tags

class Blogs(models.Model):
    title = models.TextField()
    link = models.TextField(primary_key = True)
    writer = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    text = models.CharField(max_length = 5000)
    num_responses = models.CharField(max_length = 1000)
    num_claps = models.CharField(max_length = 1000)
    tags = models.CharField(max_length=1000)
    
    def set_tags(self, x):
        self.tags = json.dumps(x)

    def __str__(self):
        return self.title