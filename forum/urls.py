from django.urls import path
from forum import views

urlpatterns = [
    path('category/<str:slug>/', views.category_post, name='category_post'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('', views.PostList.as_view(), name='index')
]
