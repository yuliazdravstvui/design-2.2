from datetime import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import RegisterUserForm, ChangeStatusRequest
from .models import Application, Category


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

class ApplicationViewUser(generic.ListView):
    model = Application
    paginate_by = 4
    template_name = 'my_application.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by('-date')

class ApplicationViewIndex(generic.ListView):
    model = Application
    paginate_by = 4
    template_name = 'index.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(status='C')

    def index(request):
        num_applications = Application.objects.filter(status='P').count()
        return render(request, 'index.html', context={'num_application': num_applications})


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['title', 'description', 'category', 'photo_file']
    template_name = 'create_application.html'
    success_url = reverse_lazy('my_application')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def create_application(request):
        return render(request, "create_application.html")

class ApplicationDelete(DeleteView):
    model = Application
    context_object_name = 'application'
    template_name = 'delete_application.html'
    success_url = reverse_lazy('my_application')

    def delete_application(self, pk):
        application = Application.objects.filter(user=self.request.user, pk=pk)
        if application:
            application.delete()
        return redirect('my_application')


class ApplicationListViewAdmin(generic.ListView):
    model = Application
    template_name = 'base.html'
    context_object_name = 'application_list'
    def get_queryset(self):
        return Application.objects.order_by('-date')[:4]

class ApplicationListView(generic.ListView):
    model = Application
    paginate_by = 4
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_application'] = Application.objects.filter(status__exact='Принято в работу').count()
        return context


class CategoryView(generic.ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

class CategoryDelete(DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category')

class CategoryCreate(CreateView):
    model = Category
    fields = ['name']
    template_name = 'creating_category.html'
    success_url = reverse_lazy('category')

class ChangeStatusRequest(UpdateView):
    model = Application
    form_class = ChangeStatusRequest
    template_name = 'change_status.html'
    success_url = reverse_lazy('admin_base')




