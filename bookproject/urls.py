from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('book', RedirectView.as_view(url='/books/', permanent=False)),
    path('book/', RedirectView.as_view(url='/books/', permanent=False)),
    path('', RedirectView.as_view(url='/books/', permanent=False)),
]