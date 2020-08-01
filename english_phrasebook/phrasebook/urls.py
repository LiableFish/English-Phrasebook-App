from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path('',
         views.index,
         name='index'),
    path('categories/',
         views.CategoriesList.as_view(),
         name='categories-list'),
    path('levels/',
         views.LevelsList.as_view(),
         name='levels-list'),
    path('themes/',
         views.ThemesList.as_view(),
         name='themes-list'),
    path('themes/<int:pk>',
         views.ThemeDetail.as_view(),
         name='theme-detail'),
    path('words/<int:pk>',
         views.WordDetail.as_view(),
         name='word-detail')
])
