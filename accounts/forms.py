# get the model currenlty active in the project which is returned using
# get_user_model from the auth
from django.contrib.auth import get_user_model
# import the inbuilt user creation from the authorisation model of django
from django.contrib.auth.forms import UserCreationForm

# class to create a user sign up form using the UserCreationForm
class UserSignUpForm(UserCreationForm):

    class Meta():
        fields = ('username','email','password1','password2')
        model = get_user_model()
    # method to set the labels using the form itself
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Display Name'
        self.fields['email'].label='Email Address'
