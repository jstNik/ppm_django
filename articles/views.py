from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView, DeleteView
from comments.models import Comment
from comments.forms import AddCommentForm, EditCommentForm
from .models import Article
from . import forms


class ArticlesListView(TemplateView):
    template_name = 'articles/list.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-postingDate')
        return render(request, self.template_name, {'articles': articles})


class ArticleDetailsView(TemplateView):
    template_name = 'articles/details.html'

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(article=article.pk).order_by('-postingDate')
        form = AddCommentForm()
        edit_forms = list()
        for comment in comments:
            edit_forms.append(EditCommentForm(initial={'pk': comment.pk, 'body': comment.body}))
        return render(request, self.template_name, {
            'article': article, 'comments': zip(comments, edit_forms), 'form': form})

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        if request.user.is_authenticated:
            if request.POST.get('pk'):
                form = EditCommentForm(data=request.POST)
                comment = Comment.objects.get(pk=request.POST.get('pk'))
                if form.is_valid() and (request.user == comment.author or request.user.is_superuser):
                    comment.body = request.POST.get('body')
                    comment.isEdited = True
                    comment.save()
                    return redirect(request.META.get('HTTP_REFERER'))
                return redirect('HTTP_REFERER')
            else:
                form = AddCommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.article = article
                comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
        url = reverse('accounts:login') + '?next=' + request.path
        return redirect(url)


class ArticleCreationView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'
    template_name = 'articles/create_edit.html'

    def get(self, request, *args, **kwargs):
        form = forms.ArticleForm
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(request.POST.get('title'))
            post.save()
            return redirect(reverse('articles:list'))
        else:
            return render(request, self.template_name, {'form': form})


class UserArticlesListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'
    template_name = 'articles/user_list.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(author=request.user)
        return render(request, self.template_name, {'articles': articles})


class EditArticleView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'
    template_name = 'articles/create_edit.html'

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        if article.author == request.user or request.user.is_superuser:
            form = forms.ArticleForm(instance=article)
            return render(request, self.template_name, {'form': form, 'article': article})
        else:
            return redirect(reverse('articles:details'), pk=article.pk, slug=article.slug)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        if article.author == request.user:
            form = forms.ArticleForm(request.POST)
            if form.is_valid():
                if request.POST.get('title') != article.title or request.POST.get('body') != article.body:
                    if request.POST.get('title') != article.title:
                        article.title = request.POST.get('title')
                        article.slug = slugify(article.title)
                    if request.POST.get('body') != article.body:
                        article.body = request.POST.get('body')
                    article.isEdited = True
                    article.save()
                    return redirect(reverse('articles:details'), pk=article.pk, slug=article.slug)
            return redirect(reverse('articles:details'), pk=article.pk, slug=article.slug)
        else:
            return redirect(reverse('articles:details'), pk=article.pk, slug=article.slug)


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'
    template_name = 'articles/delete.html'

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        if article.author == request.user or request.user.is_superuser:
            return super().get(self, request, *args, **kwargs)
        return redirect(reverse('articles:details'), pk=article.pk, slug=article.slug)

    def get_success_url(self):
        source = self.request.GET.get('source')
        if source:
            return source
        return reverse('articles:list')
