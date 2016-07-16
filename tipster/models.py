from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    upvote_balance = models.BigIntegerField(help_text="The balance from upvotes only")

    def get_net_balance(self):
        """
        Returns the net balance of the account, taking deposits and
        withdrawals into account
        """
        # TODO implement
        pass

    def recalculate_upvote_balance(self):
        # Can insert validation checks here
        pass


# class Deposit(models.Model):
#     DEPOSIT_STATUS_CHOICES = (
#         ('submitted', 'Submitted'),
#         ('approved', 'Approved'),
#         ('executed', 'Executed'),
#     )
#     profile = models.ForeignKey(Profile)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=50, default='submitted', choices=DEPOSIT_STATUS_CHOICES)


# class Withdrawal(models.Model):
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
    status = models.CharField(max_length=50, default='visible', choices=POST_STATUS_CHOICES)


class Upvote(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    index = models.IntegerField()
    amount = models.IntegerField()
    has_disbursed = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise Exception("Amount can't be less than 0")

        created = True if not self.pk else False
        if created:
            self.has_disbursed = False

        super(Upvote, self).save(*args, **kwargs)

        if created:
            self.disburse_tip()

    def disburse_tip(self):
        if self.has_disbursed:
            raise Exception("Already disbursed")

        # TODO check net balance

        # TODO implement
