from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from django.urls import reverse
from .models import *
from .forms import *
from django.views import generic
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from agents.mixins import CustomeLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class SignUpView(CreateView):
    form_class= CustomUserCreationForm
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse('login')



def LandingPage(request):

    return render(request,"landing.html")



class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    context_object_name='leads'
    template_name = "leads/lead-list.html"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False).filter(agent__user=user)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile,agent__isnull=True)
            context['unassigned']=queryset
        return context

   


class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    template_name = "leads/lead-detail.html"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
        return queryset

class LeadCreateView(CustomeLoginRequiredMixin,CreateView):
    form_class= LeadModelForm
    template_name = "leads/lead_create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        return super(LeadCreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadUpdateView(CustomeLoginRequiredMixin,UpdateView):
    model = Lead
    fields = '__all__'
    template_name = "leads/lead_update.html"

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)



class LeadDeleteView(CustomeLoginRequiredMixin,DeleteView):
    model = Lead
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)




class AssignAgentView(CustomeLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
