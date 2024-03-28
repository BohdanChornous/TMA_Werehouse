from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, CreateGoodsForm, CreateOrderForm, GoodsUpdateForms, OrdersUpdateForms
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Orders, Items, RequestRows, CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


def home(request):
    context = {
        'items': Items.objects.all()
    }
    return render(request, 'TMA_Warehous/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            role = form.cleaned_data.get('role')

            regform = {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role
                }

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, f'Email already exists')
                return render(request, 'TMA_Warehous/register.html', regform)

            try:
                validate_email(email)
            except Exception as e:
                messages.error(request, f'Email is not valid')
                return render(request, 'TMA_Warehous/register.html', regform)

            try:
                validate_password(password)
            except Exception as e:
                messages.error(request, f'Password is not valid')
                return render(request, 'TMA_Warehous/register.html', regform)

            user = CustomUser(email=email, password=make_password(password), first_name=first_name, last_name=last_name, role=int(role))
            user.save()
            messages.success(request, f'{email} registered successfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'TMA_Warehous/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'TMA_Warehous/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


class UpdateOrdersView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    form_class = OrdersUpdateForms

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2


class DeleteOrdersView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Orders
    success_url = '/orders/'

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2


class ListOfItemsView(LoginRequiredMixin, ListView):
    model = Items
    context_object_name = 'items'
    ordering = ['-item_id']


class CreateItemView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Items
    form_class = CreateGoodsForm

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2 or self.request.user.role == 0


class UpdateItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Items
    form_class = GoodsUpdateForms

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2


class DeleteItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Items
    success_url = '/goods/'

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2


class DetailItemView(LoginRequiredMixin, DetailView):
    model = Items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.object
        return context


class CreateOrderView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Orders
    form_class = CreateOrderForm
    success_message = "Request created"

    def test_func(self):
        return self.request.user.role == 1 or self.request.user.role == 2 or self.request.user.role == 0


class ListOfOrdersView(LoginRequiredMixin, ListView):
    model = Orders
    context_object_name = 'orders'
    ordering = ['-request_id']


class DetailOrdersView(LoginRequiredMixin, DetailView):
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
        return context


