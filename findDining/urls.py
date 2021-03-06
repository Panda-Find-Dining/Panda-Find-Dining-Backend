"""findDining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from api import views
from django.urls import include

router = routers.DefaultRouter()
router.register(r'meals', views.MealViewSet)
router.register(r'restaurants', views.RestaurantViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/follow/<int:pk>/', views.SaveFriendView.as_view()),
    path('api/unfollow/<int:pk>/', views.DeleteFriendView.as_view()),
    path('api/search/', views.UserSearchView.as_view(), name='search_results'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/friends/', views.UserFriendsList.as_view(),
         name='user-friend-list'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-list'),
    path('api/users/meals/', views.UserMealList.as_view(), name='user-meal-list'),
    path('api/googleapicall/<int:pk>/',
         views.GoogleAPICall.as_view(), name='google api call'),
    path('api/restaurants/<int:pk>/yes/',
         views.Yes.as_view(), name='user-list'),
    path('api/restaurants/<int:pk>/no/', views.No.as_view(), name='user-list'),
    path('api/meals/<int:pk>/match/',
         views.RestaurantMatchView.as_view(), name='matched-restaurant'),
    path('api/meals/<int:pk>/matchlist/',
         views.MatchedRestaurantList.as_view(), name='greenzone-list'),
    path('api/meals/<int:pk>/restaurants/',
         views.MealRestaurantList.as_view(), name='meal-restaurant-list'),
    path('api/meals/<int:pk>/user_selected/',
         views.UserSelectedView.as_view(), name='user-has-selected'),
    path('api/pending/', views.Pending.as_view(), name='pending'),
    path('api/match/', views.Match.as_view(), name='match'),
    path('api/decline/<int:pk>/', views.DeclineMeal.as_view(), name='decline-meal'),
    path('api/undo_yes/<int:pk>/', views.UndoYes.as_view(), name='undo-yes'),
    path('api/undo_no/<int:pk>/', views.UndoNo.as_view(), name='undo-no'),
    path('api/selected-and-match/<int:pk>/',
         views.SelectedAndMatch.as_view(), name='selected-and-match'),
    path('api/tokenpk/',
         views.TokenObtainView.as_view(), name='new-token,obtain-view'),
    path('password/reset/confirm/<str:uid>/<str:token>/', views.reset_user_password,
         name='reset_user_password'),
    path('activate/<uid>/<token>',
         views.ActivateUser.as_view({'get': 'activation'}), name='activation'),


]
