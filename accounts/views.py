from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.forms import *
from django.contrib.auth import login, logout
from accounts.forms import AccountSignupForm, DeletionForm, AccountEditForm, LoginForm
from accounts.models import Account
from articles.models import Article


class AccountSignupView(TemplateView):
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = AccountSignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AccountSignupForm(data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.profile_picture = request.FILES.get('profile_picture')
            account.save()
            login(request, account)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('articles:list')
        return render(request, self.template_name, {'form': form})


# noinspection PyBroadException
class AccountLoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            username = Account.objects.get(email=request.POST.get('username')).username
            data = request.POST.copy()
            data['username'] = username
            form = AuthenticationForm(data=data)
        except:
            form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            else:
                return redirect('articles:list')
        form = LoginForm(initial={'username': request.POST.get('username')}, data=request.POST)
        return render(request, self.template_name, {'form': form})


class AccountLogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('articles:list')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('articles:list')


class AccountProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        profile = self.kwargs.get('username')
        if profile and profile != request.user.username:
            profile = Account.objects.get(username=profile)
            articles = Article.objects.filter(author=profile.pk).order_by('-postingDate')
            account = Account.objects.get(username=profile)
            return render(request, self.template_name, {'account': account, 'articles': articles})
        return render(request, self.template_name, {'account': request.user})


class AccountEditView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountEditForm
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/edit.html'
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.kwargs.get('username'):
            if self.request.user == self.kwargs.get('username'):
                return reverse('accounts:your_profile')
            return reverse('accounts:profile', kwargs={'username': self.kwargs.get('username')})
        return reverse('accounts:your_profile')

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('username'):
            if self.kwargs.get('username') == request.user.username or request.user.is_superuser:
                return super().get(self, request, *args, **kwargs)
            return redirect('accounts:profile', username=self.kwargs.get('username'))
        return super().get(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.kwargs.get('username'):
            return Account.objects.get(username=self.kwargs.get('username'))
        return Account.objects.get(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        if self.kwargs.get('username'):
            if self.kwargs.get('username') == request.user or request.user.is_superuser:
                return super().post(self, request, *args, **kwargs)
            return redirect('accounts:profile', username=self.kwargs.get('username'))
        return super().post(self, request, *args, **kwargs)


class AccountChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    login_url = 'accounts:login'
    redirect_field_name = 'next'
    success_url = 'articles:list'


class AccountDeleteView(LoginRequiredMixin, TemplateView):
    login_url = 'account:login'
    redirect_field_name = 'next'
    template_name = 'accounts/delete.html'

    def get(self, request, *args, **kwargs):
        form = DeletionForm()
        if self.kwargs.get('username'):
            if self.kwargs.get('username') == request.user.username or request.user.is_superuser:
                return render(request, self.template_name, {'form': form})
            return redirect('accounts:profile', username=self.kwargs.get('username'))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirmed'):
            form = DeletionForm(data=request.POST)
            if form.is_valid():
                user = Account.objects.get(pk=request.user.pk)
                user.delete()
                return redirect('accounts:deletion-confirmed')
            return render(request, self.template_name, {'form': form})
        return redirect('accounts:your_profile')


class AccountDeletionConfirmedView(TemplateView):
    template_name = 'accounts/deletion_confirmed.html'
