from django.urls import path
from articles.views import ArticlesListView, ArticleDetailsView, ArticleCreationView, UserArticlesListView, \
    EditArticleView, DeleteArticleView

app_name = 'articles'

urlpatterns = [
    path('', ArticlesListView.as_view(), name='list'),
    path('articles', ArticlesListView.as_view()),
    path('articles/<int:pk>/<str:slug>', ArticleDetailsView.as_view(), name='details'),
    path('articles/create', ArticleCreationView.as_view(), name='create'),
    path('articles/your-articles', UserArticlesListView.as_view(), name='user_articles'),
    path('articles/edit/<int:pk>/<str:slug>', EditArticleView.as_view(), name='edit'),
    path('articles/delete/<int:pk>/<str:slug>', DeleteArticleView.as_view(), name='delete')
]
