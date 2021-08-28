from django.urls import path
from .views import *
app_name="leads"

urlpatterns = [
    path('',LeadListView.as_view(),name='lead-list'),
    path('lead-detail/<int:pk>',LeadDetailView.as_view(),name='lead-detail'),
    path('lead-create/',LeadCreateView.as_view(),name='lead-create'),
    path('lead-update/<int:pk>',LeadUpdateView.as_view(),name='lead-update'),
    path('lead-delete/<int:pk>',LeadDeleteView.as_view(),name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
]
