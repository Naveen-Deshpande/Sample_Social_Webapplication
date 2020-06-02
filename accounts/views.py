from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms


# Create your views here.
# signup form using create view
class SignUp(CreateView):
    # class atrribute variable assigning the created form class to an attribute
    # not instantiating the class onlu assigning the class
    form_class = forms.UserSignUpForm
    # once the usr is signed up redirect the user to the login page using the
    # reverse lazy method, which waits untill the user hits the submit btn on
    # sign up page.
    success_url = reverse_lazy('login')
    # set the template Name
    template_name = 'accounts/signup.html'
