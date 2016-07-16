from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    upvote_balance = models.BigIntegerField()


# class Deposit(models.Model):
#
#     profile = models.ForeignKey(Profile)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Withdrawal(models.Model):
#
#     profile = models.ForeignKey(Profile)
#     created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):

    POST_STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('deleted by user', 'Deleted by user'),
        ('deleted by admin', 'Deleted by admin'),
    )

    curator = models.ForeignKey(User)
    link = models.URLField()
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='visible', blank=True, choices=POST_STATUS_CHOICES)


class Upvote(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    index = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.index < 0:
            raise Exception("Amount can't be less than 0")
        super(Upvote, self).save(*args, **kwargs)
