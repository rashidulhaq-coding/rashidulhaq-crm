from .models import Lead,Agent
from django import forms
from django.forms import ValidationError, widgets
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",'first_name','last_name','email')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['email'].required=True
    



class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'profile_picture'
        )


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())


    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


    

    # def clean_profile(self):
    #     data = self.cleaned_data["profile_picture"]
    #     if data == "":
    #         raise ValidationError("Your profile picture")
    #     return data
