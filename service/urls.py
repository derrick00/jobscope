from django.urls import path
from . import views
app_name = 'jobscope'

urlpatterns = [
        path('', views.service_list, name='service_list'),
        #path('<slug:category_slug>/', views.service_list, name='service_list_by_category'),
        path('<slug:category_slug>/', views.category_list, name='category_services'),
        path('<int:id>/<slug:slug>/', views.service_detail,name='service_detail'),
        ]

