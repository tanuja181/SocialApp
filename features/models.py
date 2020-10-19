from django.db import models
from accounts.models import CustomUser
import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Post(models.Model):

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=50)
    post_image = models.ImageField('image', blank=True, null=True, default="logo.png")
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.author

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
