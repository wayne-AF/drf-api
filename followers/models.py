from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Follower model, realted to 'owner' and 'followed'.
    'owner' is a user that is following a user
    'followed' is a user that is followed by 'owner'
    We need the related_name attributes so that django can differentiate
    between 'owner' and 'followed' who both are User model instances.
    'unique_together' makes sure a user can't 'double follow' the same user
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'

