from django.shortcuts import redirect, render
from django.views.generic import *
from leads.models import Agent
from .forms import AgentModelForm
import random
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CustomeLoginRequiredMixin


# Create your views here.


class AgentListView(CustomeLoginRequiredMixin,ListView):
    model = Agent
    template_name = "agents/agent-list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDetailView(CustomeLoginRequiredMixin,DetailView):
    model = Agent
    template_name = "agents/agent-detail.html"
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(CustomeLoginRequiredMixin,CreateView):
    form_class = AgentModelForm
    template_name = "agents/agent-create.html"

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f"{random.randint(1,100000)}")
        user_email=user.email
        user.save()
        Agent.objects.create(
            user = user,
            organisation= self.request.user.userprofile 
        )    
        send_mail(
            subject='You are added as agent.',
            message='You are added to the crm as agent.',
            from_email="test@gmail.com",
            recipient_list=[user_email,],
            fail_silently=False,
            
        )
        return super().form_valid(form)



class AgentUpdateView(CustomeLoginRequiredMixin,UpdateView):
    template_name = "agents/agent-update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentDeleteView(CustomeLoginRequiredMixin,DeleteView):
    template_name = "agents/agent-delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    


    



