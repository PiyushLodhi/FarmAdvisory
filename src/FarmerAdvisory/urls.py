from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name = "login"),
    url(r"^register/$", views.register_view, name = "register"),
    url(r'^logout/$', views.logout_view, name = "logout"),
    url(r'^cropHandling/$',views.cropHandling_view, name = "cropHandling"),
    url(r'^cropPlan/$',views.cropPlan, name = "cropPlan"),
    url(r'^chatPortal/$',views.chatPortal, name = "chatPortal"),
    url(r'^ajax/addCrop/$', views.addCrop, name='addCrop'), 
    url(r'^ajax/removeCrop/$', views.removeCrop, name='removeCrop'),
    url(r'^ajax/setState/$', views.setState, name='setState'),
    url(r'^ajax/getCropData/$', views.getCropData, name='getCropData'),
    url(r'^ajax/getRecommendedCrop/$', views.getRecommendedCrop, name='getRecommendedCrop'),

]