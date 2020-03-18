from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('groups/', views.GroupList.as_view()),
    path('groups/<int:pk>/', views.GroupDetail.as_view()),
    path('cases/', views.CaseList.as_view()),
    path('cases/<int:pk>/', views.CaseDetail.as_view()),
    path('achievements/', views.AchievementList.as_view()),
    path('achievements/<int:pk>/', views.AchievementDetail.as_view()),
    path('reports/', views.AchievementList.as_view()),
    path('reports/<int:pk>/', views.AchievementDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)