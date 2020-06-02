from django.db import models
# slugify basically removes any chars that aret alph-numeric or underscores or hyphen
from django.utils.text import slugify
# misaka basically helps in link embedding (insert links)
# import misaka
# Create your models here.
# import the current user model from authorisation
from django.contrib.auth import get_user_model
from django.urls import reverse

# assifn the modelto a varibale
User = get_user_model()

# to make use of custom template tags
from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    # foreign key connecting the modelto the main group model
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    # foreign key connecting to the current user model
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')
