from django.conf import settings
from django.db import models

# Create your models here.


class Headline(models.Model):
    '''
    The headline scraped from onion.com is stored
    in this model
    '''

    title = models.CharField(max_length=120)
    image = models.ImageField()
    # we haven't used url field to make things simpler
    url = models.TextField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    '''
    associate scraping with a user to restrict
    one scrape per 24 hours
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    last_scrape = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.last_scrape)
