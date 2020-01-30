from django.contrib import admin
from django.urls import path

from .views import microfront_view, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', index, name="index"),
    path('<path:route>', microfront_view, name="microfrontend"),
]
