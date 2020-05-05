from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')

    photo = ProcessedImageField(upload_to='photos',
                                processors=[ResizeToFit(1000, 800)],
                                format='JPEG',
                                options={'quality': 100},
                                blank=False)
    
    blog_photo = ImageSpecField(source='photo',
                                processors=[ResizeToFit(600, 700)],
                                format='JPEG',
                                options={'quality': 100})

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=260)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def get_absolute_url(self, pk):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.comment
