from django.db import models
from django.conf import settings

# Create your models here.


class Note(models.Model):
    # user is owner of the note, user can own multiple notes
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    # image field is optional and can be left blank while filling the form
    image = models.ImageField(null=True, blank=True)

    url = models.URLField(null=True, blank=True)
    
    # auto fill date of creation
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self)
    def get_delete_url(self):
        return "/notes/{}/delete".format(self.pk)

    def get_update_url(self):
        return "/notes/{}/update".format(self.pk)
