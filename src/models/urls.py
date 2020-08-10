from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('FarmerAdvisory/', include('FarmerAdvisory.urls')),
    path('admin/', admin.site.urls),
    url(r'^$', login_required(TemplateView.as_view(template_name="home.html"))),
]