from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib import messages
# install django-braces module using pip install for the following
from braces.views import SelectRelatedMixin

from . import models
from . import forms

# import the current user models using get_user_model
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
# view to list the posts related to the user or all the posts
class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    # the select_related allows us to provide a tuple of related models
    # basically the foregn keys
    select_related = ('user','group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        # try fetching the related posts of the user logged in using the check
        # __iexact
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExists:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    # define the fields required to edit
    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        # save the form detials
        self.object = form.save(commit=False)
        # set the post to the user who posted
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    # set the model
    model = models.Post
    select_related = ('user','group')
    # once the user deletes the post, user is reverted backto all the posts
    success_url = reverse_lazy('posts:all')

    # these methods have pre-defined names which cannot be changed and they come
    # with the class based views to make the work easier
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    # this methods tells what will be done after deleting the post
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
