from datetime import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from .forms import RegisterUserForm
from .forms import ApplicationForm
from .models import Application


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'registration/login.html')

def logout(request):
    return render(request, 'registration/logout.html')

def registration(request):
    return render(request, 'registration.html')

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse (response)

def profile(request):
    return render(request, 'profile.html')

class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'applications'
    paginate_by = 4


class ApplicationsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'profile.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

def Application_new(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            Application = form.save(commit=False)
            Application.author = request.user
            Application.date = timezone.now()
            Application.save()
            return redirect('Application_detail', pk=Application.pk)
    else:
        form = ApplicationForm()
    return render(request, 'Application_edit.html', {'form': form})

class ApplicationDelete(ApplicationListView):
    model = Application
    context_object_name = 'application'
    template_name = 'delete.html'
    success_url = reverse_lazy('request')







