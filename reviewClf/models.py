from django.db import models

# Create your models here.

sentiment = {
    1: 'positive',
    0: 'negative'
}


class Review(models.Model):
    text = models.CharField(max_length=10000)
    label = models.IntegerField()

    def __str__(self):
        return sentiment[int(self.label)] + ": " + str(self.text)