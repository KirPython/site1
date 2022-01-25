from django.urls import path
from .views import index, by_category, detail

urlpatterns = [
    path('<int:category_id>/<int:pk>/', detail, name='detail'),
    path('<int:category_id>/', by_category, name='by_category'),
    path('', index, name='index'),
]
