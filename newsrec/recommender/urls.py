
from django.urls import path
from . import views

app_name="recommender"

urlpatterns = [
    path('', views.random_article, name='random_article'),
    path('article/<int:article_id>/', views.article_link_and_recommendations, name='article_link'),
    path('redirect/<int:article_id>/', views.redirect_to_article, name='redirect_to_article'),
]
