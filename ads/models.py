from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=350)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"[ID: {self.id}] AUTHOR: {self.user} | TITLE: {self.title} CATEGORY: {self.category}"


class ExchangeProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='receiver_proposals')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    comment = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"[ID: {self.id}] STATUS: {self.status} AD_SENDER: {self.ad_sender.id} AD_RECEIVER: {self.ad_receiver.id}"
