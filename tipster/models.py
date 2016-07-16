from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib import admin
from tipster.helpers import partition_integer_by_weights

# TODO create new type of UserException that can be exposed to the user


class Profile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    upvote_balance = models.BigIntegerField(default=0, help_text="The balance from upvotes only")

    def get_net_balance(self):
        """
        Returns the net balance of the account, taking deposits and
        withdrawals into account
        """
        deposits = Deposit.objects.filter(user=self.user, status='accepted')
        withdrawals = Withdrawal.objects.filter(user=self.user, status='executed')
        deposit_total = sum(map(lambda d: d.amount, deposits))
        withdrawal_total = sum(map(lambda w: w.amount, withdrawals))
        return self.upvote_balance + deposit_total - withdrawal_total

    def recalculate_upvote_balance(self):
        # TODO Can insert validation checks here
        pass


class Deposit(models.Model):

    DEPOSIT_STATUS_CHOICES = (
        ('received', 'Received'),
        ('accepted', 'Accepted'),
    )

    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # TODO change default to received
    status = models.CharField(max_length=50, default='accepted', choices=DEPOSIT_STATUS_CHOICES)
    amount = models.IntegerField()


class Withdrawal(models.Model):

    WITHDRAWAL_STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('executed', 'Executed'),
    )

    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='submitted', choices=WITHDRAWAL_STATUS_CHOICES)
    amount = models.IntegerField()


class Post(models.Model):

    POST_STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('deleted by user', 'Deleted by user'),
        ('deleted by admin', 'Deleted by admin'),
    )

    curator = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='visible', choices=POST_STATUS_CHOICES)

    def score(self):
        return self.upvote_set.count()

    def __str__(self):
        return "{} by {}".format(self.id, self.curator)


class Upvote(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    index = models.IntegerField()
    amount = models.IntegerField()
    has_disbursed = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.has_enough_funds():
            raise Exception("Not enough funds")
        if self.amount < 0:
            raise Exception("Insufficient amount")

        if not self.pk:
            self.has_disbursed = False

        super(Upvote, self).save(*args, **kwargs)

        if not self.has_disbursed:
            self.disburse_tip()

    def has_enough_funds(self):
        if self.user.profile.get_net_balance() - self.amount > 0 and \
                self.amount > Upvote.objects.filter(post=self.post, index__lt=self.index).count():
            return True
        else:
            return False

    def disburse_tip(self):
        if self.has_disbursed:
            raise Exception("Already disbursed")
        if not self.has_enough_funds():
            raise Exception("Not enough funds")

        tipsters = Upvote.objects.filter(post=self.post, id__lt=self.id)
        weights = {}
        for tipster in tipsters:
            weights[tipster.id] = tipster.amount

        with transaction.atomic():
            partition = partition_integer_by_weights(self.amount, weights)
            upvoter_profile = self.user.profile
            upvoter_profile.upvote_balance -= self.amount
            upvoter_profile.save()
            for tipster_id, share in partition.iteritems():
                if tipster_id == 'remainder':
                    continue
                tipster_profile = tipsters.get(id=tipster_id).user.profile
                tipster_profile.upvote_balance += share
                tipster_profile.save()

        self.has_disbursed = True
        self.save()


admin.site.register(Profile)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Post)
admin.site.register(Upvote)
