from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view),
    path('index/', views.index_view),
    path('details/', views.details_view),
    path('details_graphs/', views.details_graphs)

]
