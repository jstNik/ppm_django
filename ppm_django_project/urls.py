from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from ppm_django_project.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls'), name="homepage"),
    path('user/', include('accounts.urls')),
    path('comments/', include('comments.urls'))
] + staticfiles_urlpatterns() + static(MEDIA_URL, document_root=MEDIA_ROOT)
