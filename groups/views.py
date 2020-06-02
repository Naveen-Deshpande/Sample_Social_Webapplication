from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from groups.models import Group,GroupMember
from django.contrib import messages
from django.db import IntegrityError
from . import models


# Create your views here.
# view to create a new group, login is required
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = Group
    fields = ('name','description')

# view to display the details of a sigle created group
class SingleGroup(generic.DetailView):
    model = Group

# view to display the list of available groups
class ListGroups(generic.ListView):
    model = Group

# view to join the groups, RedirectView used to make changes to the model
# if user joins the group
class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    # pre-defined url get_redirect_url
    # once the user joins the group, will be redirected to the groups detail page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    # method to check if this person is already a member of the group
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        # try to create a group member using the user n the group
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'You are already a member of this Group!')
        else:
            messages.success(self.request,'You are now a member of the Group!')

        return super().get(request,*args,**kwargs)

# view to leave the group
class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    # once the user leaves the group, will be redirected to the groups detail page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        # try to grab the membership of the user assuming that the user is a part
        # of that group
        try:
            membership = models.GroupMember.objects.filter(
            user = self.request.user,
            group__slug = self.kwargs.get("slug")
            ).get()
        except models.GroupMember.DoesNotExists:
            messages.warning(self.request,'Sorry, you need to be a member of this group')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)
