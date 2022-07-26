from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.UserRegisterClassView.as_view(),name='register'),
    path('login/',views.UserLoginClassView.as_view(),name='login'),
    path('home/',views.HomeClassView.as_view(),name='home'),
    path('user-profile/',views.ProfileUpdateClassView.as_view(),name='user-profile'),
    path('profile-update/',views.ProfileUpdateClassView.as_view(),name='profile-update'),
    path('follow/',views.FollowClassView.as_view(),name='follow'),
    path('unfollow/',views.FollowClassView.as_view(),name='unfollow'),
    path('delete-user-account/', views.DeleteUserAccountClassView.as_view(),name='delete-user-account'),
    path('deactivate-user-account/',views.DeactivateUserAccountClassView.as_view(),name='deactivate-user-account'),
    path('activate-account/',views.EmailForActivateClassView.as_view(),name='activate-account'),
    path('activate/<uidb64>/<token>/',views.ActivateAccountClassView.as_view(), name='activate'),
    path('update-password/',views.UpdatePasswordClassView.as_view(),name='update-password'),
    path('password-reset/',views.EmailForPasswordResetClassView.as_view(),name='password-reset'),
    path('reset/<uidb64>/<token>/',views.PasswordResetClassView.as_view(),name='reset'),
    path('get-board/',views.CreateBoardClassView.as_view(),name='get-board'),
    path('create-board/',views.CreateBoardClassView.as_view(),name='create-board'),
    path('delete-board/<int:id>',views.CreateBoardClassView.as_view(),name='delete-board'),
    path('topic-list/', views.TopicListClassView.as_view(),name='topic-list'),
    path('search/',views.SearchClassView.as_view(),name='search-topic'),
]