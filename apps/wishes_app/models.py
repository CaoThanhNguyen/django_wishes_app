from django.db import models
from ..login_app.models import User

# Create your models here.
class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = "Item should have at least 3 characters"
        if len(postData['desc']) < 3:
            errors['desc'] = "Item description should have at least 3 characters"
        return errors

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="wishes")
    granted = models.BooleanField(default=False)
    granted_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

class Like(models.Model):
    wish = models.ForeignKey(Wish, related_name = "likes")
    user = models.ForeignKey(User, related_name = "users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

